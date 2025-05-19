from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from .forms import UserForm, ClienteForm, CadastroGeralForm, FinalizarCadastroClienteForm
from .models import Cliente, PersonalTrainer


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

            # Verificar se o username ou email já existem
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Este nome de usuário já está em uso.')
                return render(request, 'usuarios/cadastro_geral.html', {'form': form})
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Este e-mail já está cadastrado.')
                return render(request, 'usuarios/cadastro_geral.html', {'form': form})

            # Criar o usuário
            user = User.objects.create_user(
                username=username,
                email=email,
                password=senha,
                first_name=first_name,
                last_name=last_name,
            )

            # Criar Cliente ou Personal
            if tipo == 'cliente':
                cliente = Cliente.objects.create(user=user, peso=0, altura=0, objetivos=f'Telefone: {telefone}')
                login(request, user)
                return redirect('finalizar_cadastro_cliente', cliente_id=cliente.id)
            elif tipo == 'personal':
                trainer = PersonalTrainer.objects.create(user=user, especialidades='', precos=0, horarios='', aprovado=False)
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

    return redirect('finalizar_cadastro_cliente', user_id=cliente.id)