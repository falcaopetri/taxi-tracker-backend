from rest_framework import serializers

from api.models import *

class MotoristaSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Motorista
        fields = ('username', 'email', 'pontuacao', 'is_busy')


class PassageiroSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Passageiro
        fields = ('username', 'email')


class CorridaSerializer(serializers.ModelSerializer):
    motorista_location = serializers.CharField(source='motorista.lastKnownLocation', default='')

    class Meta:
        model = Corrida
        fields = ('status', 'origem', 'destino', 'valor', 'horarioInicial', 'horarioFinal', 'motorista', 'passageiro', 'motorista_location')
        read_only_fields = ('status', 'valor', 'horarioInicial', 'horarioFinal', 'motorista', 'passageiro')
