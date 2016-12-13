from django.db import models


class Motorista(models.Model):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=11) # TODO como adicionar máscara? (AAA.BBB.CCC-DD)
    celular = models.CharField(max_length=11) # TODO como adicionar máscara? ( (AA) BCCCC-DDDD )
    # TODO campo endereço de mensagem instantânea: tipo int?
    cnh = models.CharField(max_length=11) # TODO confirmar que CNH só tem 11 dígitos
    pontuacao = models.FloatField()

    # TODO plain-text password storing -> really bad idea
    # Check [Password management in Django](https://docs.djangoproject.com/en/1.9/topics/auth/passwords/)
    senha = models.CharField(max_length=8) # TODO confirmar requisito: qual o tamanho máximo da senha?
   

