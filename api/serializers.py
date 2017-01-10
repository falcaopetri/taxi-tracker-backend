from rest_framework import serializers

from api.models import Motorista

class MotoristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorista
        fields = ('nome', 'pontuacao')


