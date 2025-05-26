from django.contrib import admin
from .models import Cliente, PersonalTrainer, Treino, PlanoTreino, Exercicio, Especialidade, HorarioDisponivel

# Registra cada model no admin
admin.site.register(Cliente)
admin.site.register(PersonalTrainer)
admin.site.register(Treino)
admin.site.register(PlanoTreino)
admin.site.register(Exercicio)
admin.site.register(Especialidade)
admin.site.register(HorarioDisponivel)

