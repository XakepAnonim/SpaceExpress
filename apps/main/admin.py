from django.contrib import admin

from .models import Manufacturer, City, Warehouse

admin.site.register(Manufacturer)
admin.site.register(City)
admin.site.register(Warehouse)
