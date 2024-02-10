from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from .models import (
    Restaurant,
    Restaurant_image,
    MenuItems,
    Table,
    Reservation,
    ReservationMenuItem, )
from .serializers import (
    RestaurantSerializer,
    ImageSerializer,
    MenuSerializer,
    TableSerializer,
    ReservationSerializer,
    ReservationItemsSerializer, )
from rest_framework.permissions import IsAuthenticated


class restaurants_view(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            restaurants = Restaurant.objects.all()
            restaurants_serializer = RestaurantSerializer(restaurants, many=True)
            return Response(restaurants_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class detail_view(APIView):
    def get(self, request, id):
        try:
            restaurant = Restaurant.objects.get(id=id)
            serializer = RestaurantSerializer(restaurant)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class restaurant_images(APIView):
    def get(self, request, id):
        try:
            images = Restaurant_image.objects.filter(restaurant__id=id)
            serializer = ImageSerializer(images, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Restaurant_image.DoesNotExist:
            return Response({'error': 'Images not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class restaurant_menu(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            menu_items = MenuItems.objects.filter(restaurant__id=id)
            serializer = MenuSerializer(menu_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MenuItems.DoesNotExist:
            return Response({'error': 'MenuItems not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class fetch_table(APIView):
    def get(self, request, id):
        try:
            tables = Table.objects.filter(restaurant__id=id)
            serializer = TableSerializer(tables, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'No tables found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class reservation(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        table_id = request.data.get('table_id')
        date_time_str = request.data.get('datetime')
        date_time = date_time_str.replace(' at', '')
        date_time = datetime.strptime(date_time, '%B %d, %Y %I:%M %p')
        date = date_time.date()
        time = date_time.time()
        menu_items = request.data.get('menu_items', [])
        menu_items_id = [menu_item['id'] for menu_item in menu_items]
        is_table_available = Reservation.objects.filter(table__id=table_id, date=date, time=time).exists()
        if not is_table_available:
            reservation_data = {
                'user': user_id,
                'table': table_id,
                'date': date,
                'time': time,
                'status': request.data.get('status', 'pending'),
                'total': request.data.get('total', 0.0)
            }
            serializer = ReservationSerializer(data=reservation_data)
            if serializer.is_valid():
                reservation_obj = serializer.save()
                for menu_item_id in menu_items_id:
                    try:
                        menu_item_instance = MenuItems.objects.get(pk=menu_item_id)
                        reservation_obj.menu_items.add(menu_item_instance)
                    except MenuItems.DoesNotExist:
                        pass

                for menu_item in menu_items:
                    menu_item_id = MenuItems.objects.get(pk=menu_item['id'])
                    quantity = menu_item.get('quantity', 1)

                    ReservationMenuItem.objects.create(
                        reservation=reservation_obj,
                        menu_item=menu_item_id,
                        quantity=quantity
                    )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'response': 'You cannot reserve on this time'}, status=status.HTTP_400_BAD_REQUEST)


class fetch_reservations(APIView):
    def get(self, request, id):
        try:
            reservations = Reservation.objects.filter(user__id=id)
            serialized_reservations = ReservationItemsSerializer(reservations, many=True)
            return Response(serialized_reservations.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'No Reservation table found in database'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class delete_reservation(APIView):
    def delete(self, request, id):
        try:
            reservation = Reservation.objects.get(id=id)
            print('reservation*************', reservation)
            reservation.delete()
            return Response({'msg': 'Reservation Deletion Successfully'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Reservation not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
