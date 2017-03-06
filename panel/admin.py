from django.contrib import admin

from .models import Coordinates, Units, PowerExpected, PowerActual, Performance

# Register your models here.

admin.site.register(Coordinates)
admin.site.register(Units)
