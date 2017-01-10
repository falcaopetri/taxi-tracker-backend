from rest_framework import serializers

from api.models import *

class MotoristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorista
        fields = ('nome', 'pontuacao')


class PassageiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passageiro
        fields = ('login', )


class CorridaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corrida
        fields = ('status', 'origem', 'destino', 'valor', 'horarioInicial', 'horarioFinal', 'motorista', 'passageiro')
