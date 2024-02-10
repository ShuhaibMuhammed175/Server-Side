from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .email import send_otp
from .models import User
from .serializer import (
    UserRegistrationSerializer,
    VerifySerializer, )


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_admin'] = user.is_staff
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class userRegistrationView(APIView):

    def post(self, request,):
        try:
            email = request.data.get('email')
            if User.objects.filter(email=email).exists():
                return Response({"error": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = UserRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.create(serializer.validated_data)
            send_otp(serializer.validated_data['email'])
            return Response({
                "message": 'Check your email for verification',
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class verify(APIView):
    def post(self, request):
        try:
            serializer = VerifySerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data['email']
                otp = serializer.validated_data['otp']
                user = User.objects.filter(email=email)
                if not user.exists():
                    return Response({'message': 'email not found'}, status=status.HTTP_404_NOT_FOUND)
                my_user = user.first()
                if my_user.otp != otp:
                    return Response({'error': 'Invalid otp'}, status=status.HTTP_400_BAD_REQUEST)
                my_user.is_verified = True
                my_user.save()
                return Response({'email': str(email), 'message': 'Account verified'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
