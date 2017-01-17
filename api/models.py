from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime, now


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
    cooperativa = models.ForeignKey('Cooperativa',  on_delete=models.CASCADE)
    statusMotorista = models.BooleanField(default=True) 

    def __str__(self):
        return self.nome

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
    # login = models.CharField(max_length=200)
    # senha =  models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    
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

