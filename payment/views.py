import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import Reservation

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeCheckoutView(APIView):
    def post(self, request, id):
        try:
            subtotal = request.data.get('subtotal', 0)
            reservation_fee = request.data.get('reservationFee', 0)
            currency = request.data.get('currency', 'INR')

            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': currency,
                            'unit_amount': int((subtotal + reservation_fee) * 100),
                            'product_data': {
                                'name': 'FineDine',
                                'description': 'Thanks for choosing FineDine',
                            }
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=settings.SITE_URL + '/success/?payment_success=true',
                cancel_url=settings.SITE_URL + '/cancel',
            )
            reservation = Reservation.objects.get(id=id)
            reservation.status = 'confirmed'
            reservation.save()

            return Response({'id': checkout_session.id, 'url': checkout_session.url})

        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

