from django.contrib import admin
from .models import Cliente, PersonalTrainer, Especialidade, Treino, PlanoTreino, Exercicio, HorarioDisponivel

@admin.register(PersonalTrainer)
class PersonalTrainerAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefone', 'aprovado')
    list_filter = ('aprovado', 'especialidades')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    filter_horizontal = ('especialidades',)
    list_editable = ('aprovado',)

admin.site.register(Cliente)
admin.site.register(Especialidade)
admin.site.register(Treino)
admin.site.register(PlanoTreino)
admin.site.register(Exercicio)
admin.site.register(HorarioDisponivel)


