from .models import Sala, Reservacion, User
from rest_framework import serializers


class SalaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sala
        fields = ['id', 'nombre', 'descripcion', 'capacidad']


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user


class ReservacionSerializer(serializers.HyperlinkedModelSerializer):
    usuario = UserSerializer()

    class Meta:
        model = Reservacion
        fields = ['id', 'sala', 'usuario', 'inicio', 'fin', 'activa']

    def validate(self, data):
        """
        Check that there's not another reservation for same room in same range of time and the same room
        """
        #OrderedDict([('sala', < Sala: Sala A, capacidad: 5 >),
        #             ('usuario', OrderedDict([('email', 'cesar@local.com'), ('username', 'cesar')])),
        #             ('inicio', datetime.datetime(2020, 1, 12, 11, 5, tzinfo= < UTC >)), (
        #'fin', datetime.datetime(2020, 1, 13, 12, 8, tzinfo= < UTC >)), ('activa', True)])
        sala = data['sala']
        inicio = data['inicio']
        fin = data['fin']
        reservas = Reservacion.objects.filter(sala=sala)
        reservas = reservas.filter(inicio__range=[inicio, fin]) | reservas.filter(fin__range=[inicio, fin])
        reserva = reservas.first()
        if reserva:
            raise serializers.ValidationError("Ya existe una reunion en esa sala al mismo tiempo")
        return data


    def create(self, validated_data):
        # the request already was validated on client and have existing user
        usuario = validated_data.pop('usuario')
        user = User.objects.filter(username=usuario['username']).first()
        reservacion = Reservacion(**validated_data)
        reservacion.usuario = user
        reservacion.save()
        return reservacion

    def update(self, instance, validated_data):
        # solo actualizaremos su status
        instance.activa = validated_data.get('activa', instance.activa)
        instance.save()
        return instance
