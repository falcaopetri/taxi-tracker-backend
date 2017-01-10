from django.shortcuts import render

from rest_framework import viewsets

from api.models import Motorista
from api.serializers import MotoristaSerializer

class MotoristaViewSet(viewsets.ModelViewSet):
    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer


