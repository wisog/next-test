from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, status

from salas.serializers import SalaSerializer, ReservacionSerializer, UserSerializer
from .models import Sala, Reservacion, User


class SalaViewSet(viewsets.ModelViewSet):
    """
    API endpoint - Permite crear y consultar salas.
    """
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    permission_classes = [IsAuthenticated]



class ReservacionViewSet(viewsets.ModelViewSet):

    queryset = Reservacion.objects.all()
    serializer_class = ReservacionSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, reservacion_id=None):
        reservacion = self.queryset.filter(id = reservacion_id).first()
        if reservacion:
            serializer = self.get_serializer(reservacion)
            return Response(serializer.data)
        return Response({
            'status': False,
            'message': 'not found or deleted'  # 'Reservacion was not found.'
        }, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, reservacion_id=None):
        reservacion = self.queryset.filter(id = reservacion_id).first()
        if reservacion:
            serializer = self.get_serializer(reservacion)
            activa = request.data['activa']
            reservacion.activa = activa
            reservacion.save()
            return Response(serializer.data)
        return Response({
            'status': False,
            'message': 'not found or deleted'  # 'Reservacion was not found.'
        }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, reservacion_id=None):
        return Response({
            'status': False,
            'message': 'not supported yet'  # Reservacion was not found.
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint - Permite crear y consultar usuarios.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


def index(request):
    template = loader.get_template('salas/index.html')
    context = {
        'user': settings.API_CREDENTIALS['user'],
        'password': settings.API_CREDENTIALS['password']
    }
    return HttpResponse(template.render(context, request))
