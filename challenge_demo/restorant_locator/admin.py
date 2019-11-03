from django.contrib import admin
from restorant_locator.models import Restaurant


@admin.register(Restaurant)
class AdminRestaurant(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'created', 'modified')
