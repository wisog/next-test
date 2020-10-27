from django.urls import include, path
from rest_framework import routers
from . import views

from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()
router.register(r'salas', views.SalaViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', views.index),
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'api/v1/reservaciones/', csrf_exempt(views.ReservacionViewSet.as_view({'get': 'list', 'post': 'create'})), name='reservacion'),
    path(r'api/v1/reservaciones/<int:reservacion_id>/', csrf_exempt(views.ReservacionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'delete'})), name='reservacion'),
]