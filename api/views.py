from django.shortcuts import render

from rest_framework import viewsets

from api.models import *
from api.serializers import *


class MotoristaViewSet(viewsets.ModelViewSet):
    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer


class PassageiroViewSet(viewsets.ModelViewSet):
    queryset = Passageiro.objects.all()
    serializer_class = PassageiroSerializer


class CorridaViewSet(viewsets.ModelViewSet):
    queryset = Corrida.objects.all()
    serializer_class = CorridaSerializer
