from django.urls import path
from . import views

urlpatterns = [
    path('create-checkout-session/<int:id>/', views.StripeCheckoutView.as_view())
]
