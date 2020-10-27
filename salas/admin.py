from django.contrib import admin

from .models import Sala, Reservacion, User

admin.site.register(Sala)
admin.site.register(Reservacion)
admin.site.register(User)
