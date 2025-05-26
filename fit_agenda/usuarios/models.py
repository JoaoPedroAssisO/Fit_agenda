from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=4, decimal_places=2)
    objetivos = models.TextField()

    def __str__(self):
        return f"Cliente: {self.user.username}"


class PersonalTrainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20)
    especialidades = models.TextField()
    precos = models.DecimalField(max_digits=6, decimal_places=2)
    aprovado = models.BooleanField(default=False) 
    

    def __str__(self):
        return f"Personal Trainer: {self.user.username}"
    
class Treino(models.Model):
    MODALIDADES = [
        ('presencial', 'Presencial'),
        ('online', 'Online'),
    ]

    STATUS = [
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('concluido', 'Concluído'),
    ]

    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    trainer = models.ForeignKey('PersonalTrainer', on_delete=models.CASCADE)
    data_horario = models.DateTimeField()
    modalidade = models.CharField(max_length=20, choices=MODALIDADES)
    status = models.CharField(max_length=20, choices=STATUS)

    def __str__(self):
        return f"Treino de {self.cliente.user.username} com {self.trainer.user.username} em {self.data_horario.strftime('%d/%m/%Y %H:%M')}"
    
class PlanoTreino(models.Model):
    cliente = models.ForeignKey('usuarios.Cliente', on_delete=models.CASCADE)
    trainer = models.ForeignKey('usuarios.PersonalTrainer', on_delete=models.CASCADE)
    data = models.DateField()
    observacoes = models.TextField(blank=True)

    def __str__(self):  # <-- aqui estava fora da classe
        return f"Plano de treino de {self.cliente.user.username} com {self.trainer.user.username} em {self.data.strftime('%d/%m/%Y')}"

class Exercicio(models.Model):
    plano = models.ForeignKey('PlanoTreino', on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    series = models.IntegerField()
    repeticoes = models.IntegerField()
    carga = models.DecimalField(max_digits=5, decimal_places=2)
    video_url = models.URLField(blank=True, null=True)  # Campo opcional

    def __str__(self):
        return f"Exercício: {self.nome}"
    
class Especialidade(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()

    def __str__(self):
        return self.nome
    


class HorarioDisponivel(models.Model):
    trainer = models.ForeignKey(PersonalTrainer, on_delete=models.CASCADE, related_name='horarios_disponiveis')
    
    dia_semana = models.CharField(
        max_length=10,
        choices=[
            ('segunda', 'Segunda-feira'),
            ('terca', 'Terça-feira'),
            ('quarta', 'Quarta-feira'),
            ('quinta', 'Quinta-feira'),
            ('sexta', 'Sexta-feira'),
            ('sabado', 'Sábado'),
            ('domingo', 'Domingo'),
        ]
    )

    horario_inicio_manha = models.TimeField(null=True, blank=True)
    horario_fim_manha = models.TimeField(null=True, blank=True)

    horario_inicio_tarde = models.TimeField(null=True, blank=True)
    horario_fim_tarde = models.TimeField(null=True, blank=True)

    horario_inicio_noite = models.TimeField(null=True, blank=True)
    horario_fim_noite = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.trainer.user.username} - {self.dia_semana}"


