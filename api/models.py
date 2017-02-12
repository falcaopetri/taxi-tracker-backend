from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime, now


class Motorista(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cpf = models.CharField(max_length=11, default='') # TODO como adicionar máscara? (AAA.BBB.CCC-DD)
    celular = models.CharField(max_length=11, default='') # TODO como adicionar máscara? ( (AA) BCCCC-DDDD )
    # TODO campo endereço de mensagem instantânea: tipo int?
    cnh = models.CharField(max_length=11, default='') # TODO confirmar que CNH só tem 11 dígitos
    pontuacao = models.FloatField(default=-1)

    statusMotorista = models.BooleanField(default=True) 

    lastKnownLocation = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.user.username

    @property
    def is_busy(self):
        corridas_espera = self.corrida_set.filter(status=Corrida.ESPERA)
        corridas_iniciada = self.corrida_set.filter(status=Corrida.INICIADA)

        return len(corridas_espera) == 0 and len(corridas_iniciada) == 0


class Cooperativa(models.Model):
    nome = models.CharField(max_length=200)
    endereco = models.CharField(max_length=200)
    telefone = models.CharField(max_length=10)
    login = models.CharField(max_length=20)
    senha = models.CharField(max_length=30)
    def __str__(self):
        return self.nome


class Veiculo(models.Model):
    LICENCIADO = 'licenciado'
    NLICENCIADO = 'n_licenciado'
    STATUS_CHOICES = (
        (LICENCIADO, 'Licenciado'),
        (NLICENCIADO,  'Não Licenciado'),
    )
    modelo  = models.CharField(max_length=200)
    marca  = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices = STATUS_CHOICES,
        default=NLICENCIADO
    )
    cooperativa = models.ForeignKey('Cooperativa', on_delete=models.CASCADE)
    def __str__(self):
        return self.modelo

class Uso(models.Model):
	dataInicio = models.DateField(null=True, blank=True)
	dataInicio = models.DateField(null=True, blank=True)

	veiculo = models.ForeignKey('Veiculo', on_delete=models.CASCADE)
	motorista = models.ForeignKey('Motorista', on_delete=models.CASCADE)
	
	
class Passageiro(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def has_active_race(self):
        corridas_espera = self.corrida_set.filter(status=Corrida.ESPERA)
        corridas_iniciada = self.corrida_set.filter(status=Corrida.INICIADA)

        return len(corridas_espera) == 0 and len(corridas_iniciada) == 0
    
class Corrida(models.Model):
    ESPERA = 'em_espera'
    CANCELADA = 'cancelada'
    INICIADA = 'iniciada'
    FINALIZADA = 'finalizada'
    STATUS_CHOICES = (
        (ESPERA, 'Em Espera'),
        (CANCELADA, 'Cancelada'),
        (INICIADA, 'Iniciada'),
        (FINALIZADA, 'Finalizada'),
    )
    status = models.CharField(
        max_length=20,
        choices = STATUS_CHOICES, 
        default = ESPERA
    )

    origem = models.CharField(max_length=200)
    destino = models.CharField(max_length=200)

    valor = models.FloatField(default=0.0)	

    horarioInicial = models.DateField(null=True, blank=True)
    horarioFinal = models.DateField(null=True, blank=True)

    pontuacao = models.FloatField(default=0.0)

    motorista = models.ForeignKey(Motorista, null=True)
    passageiro = models.ForeignKey(Passageiro, null=True)

