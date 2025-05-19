# usuarios/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Cliente

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['peso', 'altura', 'objetivos']


TIPOS_USUARIO = [
    ('cliente', 'Cliente'),
    ('personal', 'Personal Trainer'),
]

class CadastroGeralForm(forms.Form):
    first_name = forms.CharField(label='Primeiro nome', max_length=30)
    last_name = forms.CharField(label='Sobrenome', max_length=30)
    telefone = forms.CharField(label='Telefone', max_length=15)
    email = forms.EmailField(label='Email')
    username = forms.CharField(label='Nome de usuário', max_length=30)
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)
    tipo_usuario = forms.ChoiceField(label='Tipo de usuário', choices=TIPOS_USUARIO)
    

class FinalizarCadastroClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['peso', 'altura', 'objetivos']