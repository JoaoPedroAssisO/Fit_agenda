from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.forms import modelformset_factory
from .forms import UserForm, ClienteForm, CadastroGeralForm, FinalizarCadastroClienteForm, FinalizarCadastroPersonalForm, HorarioDisponivelForm
from .models import Cliente, PersonalTrainer, HorarioDisponivel, Treino, Especialidade
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
import json
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.db import models





# Cria a view para o login
def login_view(request):
    alerta_personal_nao_aprovado = False  # Flag para exibir JS alert

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # Redirecionamento com base no perfil do usuário
                if hasattr(user, 'cliente'):
                    return redirect('dashboard_cliente')
                elif hasattr(user, 'personaltrainer'):
                    if user.personaltrainer.aprovado:
                        return redirect('dashboard_personal')
                    else:
                        logout(request)  # Desloga imediatamente
                        alerta_personal_nao_aprovado = True
                else:
                    messages.error(request, 'Seu perfil não foi identificado.')
                    return redirect('login')
        else:
            messages.error(request, 'Erro no formulário. Verifique os dados.')

    else:
        form = AuthenticationForm()

    return render(request, 'usuarios/login.html', {
        'form': form,
        'alerta_personal_nao_aprovado': alerta_personal_nao_aprovado
    })



# Cria a view para o cadastro
def cadastro_geral(request):
    if request.method == 'POST':
        form = CadastroGeralForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            telefone = form.cleaned_data['telefone']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            senha = form.cleaned_data['senha']

            # Use diretamente do POST
            tipo = request.POST.get('tipo_usuario')

            # Verificações de unicidade
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Este nome de usuário já está em uso.')
                return render(request, 'usuarios/cadastro_geral.html', {'form': form})

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Este e-mail já está cadastrado.')
                return render(request, 'usuarios/cadastro_geral.html', {'form': form})

            # Criação do usuário
            user = User.objects.create_user(
                username=username,
                email=email,
                password=senha,
                first_name=first_name,
                last_name=last_name,
            )

            if tipo == 'cliente':
                cliente = Cliente.objects.create(user=user, telefone=telefone, peso=0, altura=0, objetivos='')
                login(request, user)
                return redirect('finalizar_cadastro_cliente', user_id=user.id)

            elif tipo == 'personal':
                trainer = PersonalTrainer.objects.create(user=user, telefone=telefone, precos=0, aprovado=False)
                login(request, user)
                return redirect('finalizar_cadastro_personal', trainer_id=trainer.id)

    else:
        form = CadastroGeralForm()

    return render(request, 'usuarios/cadastro_geral.html', {'form': form})




def finalizar_cadastro_cliente(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    cliente = get_object_or_404(Cliente, user=user)

    if request.method == 'POST':
        form = FinalizarCadastroClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('dashboard_cliente')  # Redireciona para o dashboard após salvar
    else:
        form = FinalizarCadastroClienteForm(instance=cliente)

    return render(request, 'usuarios/finalizar_cadastro_cliente.html', {'form': form})


def finalizar_cadastro_personal(request, trainer_id):
    trainer = get_object_or_404(PersonalTrainer, pk=trainer_id)

    if request.method == 'POST':
        form = FinalizarCadastroPersonalForm(request.POST, instance=trainer)
        if form.is_valid():
            form.save()
            return redirect('login')  # ou outra página de sucesso
    else:
        form = FinalizarCadastroPersonalForm(instance=trainer)

    return render(request, 'usuarios/finalizar_cadastro_personal.html', {'form': form})


class HorarioDisponivelForm(forms.ModelForm):
    class Meta:
        model = HorarioDisponivel
        fields = [
            'dia_semana',
            'horario_inicio_manha', 'horario_fim_manha',
            'horario_inicio_tarde', 'horario_fim_tarde',
            'horario_inicio_noite', 'horario_fim_noite',
        ]
        widgets = {
            'dia_semana': forms.HiddenInput(),
            'horario_inicio_manha': forms.TimeInput(attrs={'type': 'time'}),
            'horario_fim_manha': forms.TimeInput(attrs={'type': 'time'}),
            'horario_inicio_tarde': forms.TimeInput(attrs={'type': 'time'}),
            'horario_fim_tarde': forms.TimeInput(attrs={'type': 'time'}),
            'horario_inicio_noite': forms.TimeInput(attrs={'type': 'time'}),
            'horario_fim_noite': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields:
            if 'horario_' in campo:
                self.fields[campo].required = False




def finalizar_cadastro_personal(request, trainer_id):
    if request.method == 'POST':
        print("🔁 [POST RECEBIDO]")
        print("📦 Dados do POST:")
        for k, v in request.POST.items():
            print(f"{k}: {v}")

    trainer = get_object_or_404(PersonalTrainer, pk=trainer_id)

    HorarioFormSet = modelformset_factory(
        HorarioDisponivel,
        form=HorarioDisponivelForm,
        extra=0,
        can_delete=True,
    )

    # Garante que existam horários para todos os dias da semana (para mostrar no formset)
    dias_semana = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']
    for dia in dias_semana:
        HorarioDisponivel.objects.get_or_create(trainer=trainer, dia_semana=dia)

    horarios_qs = HorarioDisponivel.objects.filter(trainer=trainer).order_by('id')

    if request.method == 'POST':
        form = FinalizarCadastroPersonalForm(request.POST, instance=trainer)
        formset = HorarioFormSet(request.POST, queryset=horarios_qs)

        print("✅ Formulário principal é válido?", form.is_valid())
        print("✅ Formset é válido?", formset.is_valid())

        if not formset.is_valid():
            print("❌ Erros no formset:")
            for subform in formset:
                print(subform.errors)

        if form.is_valid() and formset.is_valid():
            especialidades_ids = request.POST.get('especialidades', '').split(',')
            especialidades_ids = list(filter(None, especialidades_ids))
            especialidades_ids = list(map(int, especialidades_ids))
            form.save()
            trainer.especialidades.set(especialidades_ids)
            horarios = formset.save(commit=False)

            for horario in horarios:
                horario.trainer = trainer

                print("📅 Verificando horários preenchidos para:", horario.dia_semana)
                print(f"   Manhã: {horario.horario_inicio_manha} - {horario.horario_fim_manha}")
                print(f"   Tarde: {horario.horario_inicio_tarde} - {horario.horario_fim_tarde}")
                print(f"   Noite: {horario.horario_inicio_noite} - {horario.horario_fim_noite}")

                if any([
                    horario.horario_inicio_manha, horario.horario_fim_manha,
                    horario.horario_inicio_tarde, horario.horario_fim_tarde,
                    horario.horario_inicio_noite, horario.horario_fim_noite,
                ]):
                    horario.save()
                    print("✅ Horário salvo.")
                else:
                    if horario.pk:
                        horario.delete()
                        print("🗑️ Horário vazio excluído.")

            for obj in formset.deleted_objects:
                obj.delete()
                print(f"🗑️ Horário removido via checkbox: {obj}")

            return redirect('login')

    else:
        form = FinalizarCadastroPersonalForm(instance=trainer)
        formset = HorarioFormSet(queryset=horarios_qs)

    return render(request, 'usuarios/finalizar_cadastro_personal.html', {
        'form': form,
        'formset': formset,
    })


def dashboard_cliente(request):
    # Verifica se o usuário está logado e é cliente
    if not request.user.is_authenticated:
        return redirect('login')

    # Verifica se o usuário tem perfil de cliente
    if not hasattr(request.user, 'cliente'):
        # Se não for cliente, pode redirecionar para outra página, por exemplo
        return redirect('login')

    # Renderiza o template do dashboard do cliente
    return render(request, 'usuarios/dashboard_cliente.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def editar_perfil(request):
    cliente = get_object_or_404(Cliente, user=request.user)

    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.email = request.POST.get('email', '').strip()
        user.save()

        cliente.peso = request.POST.get('peso', '').strip()
        cliente.altura = request.POST.get('altura', '').strip()
        cliente.objetivos = request.POST.get('objetivos', '').strip()
        cliente.save()

        return JsonResponse({'mensagem': 'Perfil atualizado com sucesso'})

    return render(request, 'usuarios/editar_perfil_ajax.html', {
        'cliente': cliente,
        'user': request.user  # agora você pode usar {{ user.first_name }} no template
    })

@login_required
def agendar_treino(request):
    if request.method == 'POST':
        cliente = request.user.cliente
        personal_id = request.POST.get('personal')
        data = request.POST.get('data')
        horario = request.POST.get('horario')
        modalidade = request.POST.get('modalidade')

        if not all([personal_id, data, horario, modalidade]):
            return JsonResponse({'mensagem': 'Todos os campos são obrigatórios.'}, status=400)

        try:
            # Junta data e horário e converte para datetime aware
            data_horario_str = f"{data} {horario}"
            dt_final = timezone.make_aware(datetime.strptime(data_horario_str, "%Y-%m-%d %H:%M"))

            # Verifica se já existe um treino marcado com esse personal nesse horário
            conflito = Treino.objects.filter(
                trainer_id=personal_id,
                data_horario=dt_final
            ).exists()

            if conflito:
                return JsonResponse({'mensagem': 'Esse horário já está ocupado para esse personal. Por favor, escolha outro.'}, status=409)

            # Cria o treino
            Treino.objects.create(
                cliente=cliente,
                trainer_id=personal_id,
                data_horario=dt_final,
                modalidade=modalidade,
                status='confirmado'
            )

            return JsonResponse({'mensagem': 'Treino agendado com sucesso!'})
        except Exception as e:
            return JsonResponse({'mensagem': f'Erro ao salvar treino: {str(e)}'}, status=500)

    # GET
    especializacoes = Especialidade.objects.all()
    trainers = PersonalTrainer.objects.filter(aprovado=True)
    return render(request, 'usuarios/agendar_treino_ajax.html', {
        'especializacoes': especializacoes,
        'trainers': trainers
    })




@login_required
def horarios_disponiveis(request):
    personal_id = request.GET.get('personal_id')
    data_str = request.GET.get('data')  # ex: '2025-06-20'

    try:
        trainer = PersonalTrainer.objects.get(id=personal_id)
        data_obj = datetime.strptime(data_str, "%Y-%m-%d").date()
        dia_semana = data_obj.strftime('%A').lower()

        traducoes = {
            'monday': 'segunda',
            'tuesday': 'terca',
            'wednesday': 'quarta',
            'thursday': 'quinta',
            'friday': 'sexta',
            'saturday': 'sabado',
            'sunday': 'domingo'
        }
        dia_semana_pt = traducoes.get(dia_semana, dia_semana)

        horarios = HorarioDisponivel.objects.filter(trainer=trainer, dia_semana=dia_semana_pt).first()
        if not horarios:
            return JsonResponse({'horarios': []})

        # horários já ocupados
        treinos_marcados = Treino.objects.filter(
            trainer=trainer,
            data_horario__date=data_obj
        ).values_list('data_horario__time', flat=True)

        horarios_livres = []

        def gerar_intervalos(inicio, fim):
            lista = []
            atual = datetime.combine(data_obj, inicio)
            limite = datetime.combine(data_obj, fim)
            while atual <= limite:
                if atual.time() not in treinos_marcados:
                    lista.append(atual.strftime('%H:%M'))
                atual += timedelta(hours=1)
            return lista

        for inicio, fim in [
            (horarios.horario_inicio_manha, horarios.horario_fim_manha),
            (horarios.horario_inicio_tarde, horarios.horario_fim_tarde),
            (horarios.horario_inicio_noite, horarios.horario_fim_noite)
        ]:
            if inicio and fim:
                horarios_livres.extend(gerar_intervalos(inicio, fim))

        return JsonResponse({'horarios': horarios_livres})

    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=400)



@login_required
def obter_personais(request):
    especializacao_id = request.GET.get('especializacao')
    personais = PersonalTrainer.objects.filter(especialidades__id=especializacao_id, aprovado=True)

    data = [{
        'id': p.id,
        'nome': p.user.get_full_name(),
        'preco': float(p.precos)
    } for p in personais]

    return JsonResponse({'personais': data})

@login_required
def obter_horarios(request):
    personal_id = request.GET.get('personal_id')
    data = request.GET.get('data')  # 'YYYY-MM-DD'

    # Lógica simulada
    horarios_disponiveis = ['08:00', '10:00', '14:00', '16:00']

    return JsonResponse({'horarios': horarios_disponiveis})


@login_required
@require_POST
def cancelar_treino(request):
    treino_id = request.POST.get('treino_id')

    try:
        treino = Treino.objects.get(id=treino_id, cliente=request.user.cliente)
        treino.status = 'cancelado'
        treino.save()
        return JsonResponse({'mensagem': 'Treino cancelado com sucesso.'})
    except Treino.DoesNotExist:
        return JsonResponse({'erro': 'Treino não encontrado ou você não tem permissão.'}, status=404)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)

@login_required
def atividades_cliente(request):
    cliente = request.user.cliente
    treinos = Treino.objects.filter(cliente=cliente).order_by('-data_horario')

    return render(request, 'usuarios/atividade_cliente_ajax.html', {
        'treinos': treinos
    })

@login_required
def dashboard_personal(request):
    if not hasattr(request.user, 'personaltrainer'):
        return redirect('login')

    personal = request.user.personaltrainer
    treinos = Treino.objects.filter(trainer=personal).order_by('data_horario')

    return render(request, 'usuarios/dashboard_personal.html', {
        'personal': personal,
        'treinos': treinos
    })


@login_required
def editar_perfil_personal(request):
    personal = get_object_or_404(PersonalTrainer, user=request.user)

    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.email = request.POST.get('email', '').strip()
        user.save()

        return JsonResponse({'mensagem': 'Perfil atualizado com sucesso!'})

    return render(request, 'usuarios/editar_perfil_personal_ajax.html', {
        'user': request.user
    })

@login_required
@require_POST
def editar_dados_personal(request):
    personal = request.user.personaltrainer

    try:
        # Atualiza preço e especialidades
        preco = request.POST.get("precos")
        especialidades_ids = request.POST.getlist("especialidades")
        personal.precos = preco
        personal.save()
        personal.especialidades.set(especialidades_ids)

        # Atualiza horários
        for dia in HorarioDisponivel.objects.filter(trainer=personal):
            dia.horario_inicio_manha = request.POST.get(f"manha_inicio_{dia.id}") or None
            dia.horario_fim_manha = request.POST.get(f"manha_fim_{dia.id}") or None
            dia.horario_inicio_tarde = request.POST.get(f"tarde_inicio_{dia.id}") or None
            dia.horario_fim_tarde = request.POST.get(f"tarde_fim_{dia.id}") or None
            dia.horario_inicio_noite = request.POST.get(f"noite_inicio_{dia.id}") or None
            dia.horario_fim_noite = request.POST.get(f"noite_fim_{dia.id}") or None
            dia.save()

        return JsonResponse({"mensagem": "Dados atualizados com sucesso!"})
    
    except Exception as e:
        return JsonResponse({"erro": f"Erro ao salvar dados: {str(e)}"}, status=500)



@login_required
def editar_dados_form(request):
    personal = request.user.personaltrainer

    # Garante que existem horários para os 7 dias
    dias_semana = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']
    for dia in dias_semana:
        HorarioDisponivel.objects.get_or_create(trainer=personal, dia_semana=dia)

    especializacoes = Especialidade.objects.all()

    # ⚠️ ESSA parte é essencial
    horarios = HorarioDisponivel.objects.filter(trainer=personal).order_by(
        models.Case(
            *[models.When(dia_semana=d, then=pos) for pos, d in enumerate(dias_semana)]
        )
    )

    return render(request, 'usuarios/editar_dados_personal_ajax.html', {
        'personal': personal,
        'especializacoes': especializacoes,
        'horarios': horarios,
    })



