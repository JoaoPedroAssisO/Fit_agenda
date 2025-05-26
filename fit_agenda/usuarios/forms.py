# usuarios/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Cliente, PersonalTrainer,  HorarioDisponivel

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
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    telefone = forms.CharField(max_length=20)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    senha = forms.CharField(widget=forms.PasswordInput)
    tipo_usuario = forms.ChoiceField(choices=[('cliente', 'Cliente'), ('personal', 'Personal Trainer')])

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username
    

class FinalizarCadastroClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['peso', 'altura', 'objetivos']


class FinalizarCadastroPersonalForm(forms.ModelForm):
    class Meta:
        model = PersonalTrainer
        fields = ['especialidades', 'precos']


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