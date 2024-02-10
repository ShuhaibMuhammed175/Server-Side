from django.urls import path
from . import views

urlpatterns = [
    path('restaurants/', views.restaurants_view.as_view(), name='restaurants'),
    path('restaurant/<int:id>/', views.detail_view.as_view(), name='restaurant_detail_view'),
    path('restaurant/images/<int:id>/', views.restaurant_images.as_view(), name='restaurant_images'),
    path('restaurant/menu_items/<int:id>/', views.restaurant_menu.as_view(), name='restaurant_menu'),
    path('restaurant/tables/<int:id>/', views.fetch_table.as_view(), name='fetch_table'),
    path('restaurant/reservation/', views.reservation.as_view(), name='reservation'),
    path('reservations/<int:id>/', views.fetch_reservations.as_view(), name='reservations'),
    path('reservation/delete/<int:id>/', views.delete_reservation.as_view(), name='reservation_delete')
]
