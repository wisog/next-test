from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(blank=False, default='test_user', max_length=50)

    def __str__(self):
        return self.first_name + ' ' + self.email


class Sala(models.Model):
    nombre = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=200)
    capacidad = models.IntegerField()

    class Meta:
        permissions = [
            ("crear_sala", "Puede crear salas"),
            ("editar_sala", "Puede editar informacion de las salas"),
            ("eliminar_sala", "Puede eliminar salas"),
        ]

    def __str__(self):
        return "%s, capacidad: %d" % (self.nombre, self.capacidad)


class Reservacion(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    activa = models.BooleanField(default=True)



class Historial(models.Model):
    reservacion = models.ForeignKey(Reservacion, on_delete=models.DO_NOTHING)
    duracion = models.IntegerField()  # Duracion real en minutos


