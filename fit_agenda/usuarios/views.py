from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.forms import modelformset_factory
from .forms import UserForm, ClienteForm, CadastroGeralForm, FinalizarCadastroClienteForm, FinalizarCadastroPersonalForm, HorarioDisponivelForm
from .models import Cliente, PersonalTrainer, HorarioDisponivel


# Cria a view para o login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Usando AuthenticationForm
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # ou qualquer página após login
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        else:
            messages.error(request, 'Erro no formulário. Verifique os dados.')
    else:
        form = AuthenticationForm()  # Caso seja GET, exibe o formulário vazio

    return render(request, 'usuarios/login.html', {'form': form})


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
            tipo = form.cleaned_data['tipo_usuario']

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
                trainer = PersonalTrainer.objects.create(user=user,telefone=telefone,especialidades='',precos=0,aprovado=False)
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
            return redirect('login')  # ou outra página de sucesso
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
      print("DADOS POSTADOS:")
      print(request.POST)
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

        if form.is_valid() and formset.is_valid():
            form.save()

            horarios = formset.save(commit=False)

            for horario in horarios:
                horario.trainer = trainer
                # Só salva se algum horário estiver preenchido para evitar salvar vazio
                if any([
                    horario.horario_inicio_manha, horario.horario_fim_manha,
                    horario.horario_inicio_tarde, horario.horario_fim_tarde,
                    horario.horario_inicio_noite, horario.horario_fim_noite,
                ]):
                    horario.save()
                else:
                    # Se o registro existe e está vazio, deleta para não poluir a base
                    if horario.pk:
                        horario.delete()

            # Apaga objetos excluídos via formset (se usou checkbox para deletar)
            for obj in formset.deleted_objects:
                obj.delete()

            return redirect('login')  # Ou para onde quiser

    else:
        form = FinalizarCadastroPersonalForm(instance=trainer)
        formset = HorarioFormSet(queryset=horarios_qs)

    return render(request, 'usuarios/finalizar_cadastro_personal.html', {
        'form': form,
        'formset': formset,
    })

