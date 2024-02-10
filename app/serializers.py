from rest_framework import serializers
from .models import (
    Restaurant,
    Restaurant_location,
    Restaurant_image,
    MenuItems,
    Table,
    Reservation, )


class RestaurantLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant_location
        fields = ['location']


class RestaurantSerializer(serializers.ModelSerializer):
    location = serializers.StringRelatedField(source='location.location')

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'profile_image', 'location', 'phone_number', 'email', 'description', 'address',
                  'opening_time', 'closing_time']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant_image
        fields = ['image']


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItems
        exclude = ['restaurant']


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        exclude = ['restaurant']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


class ReservationMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItems
        fields = ['id', 'name']


class ReservationItemsSerializer(serializers.ModelSerializer):
    menu_items = ReservationMenuSerializer(many=True, read_only=True)
    restaurant_name = serializers.StringRelatedField(source='table.restaurant.name')
    table_no = serializers.StringRelatedField(source='table.table_no')

    class Meta:
        model = Reservation
        fields = ['id', 'restaurant_name', 'table_no', 'date', 'time', 'menu_items', 'status', 'total']
