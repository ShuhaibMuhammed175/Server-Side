from django.contrib import admin
from .models import (
    Restaurant,
    Restaurant_location,
    Restaurant_image,
    MenuItems,
    Reservation,
    ReservationMenuItem,
    Table,)

admin.site.register(Restaurant)
admin.site.register(Restaurant_location)
admin.site.register(Restaurant_image)
admin.site.register(MenuItems)
admin.site.register(Reservation)
admin.site.register(ReservationMenuItem)
admin.site.register(Table)
