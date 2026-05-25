from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Cidadao, Servidor, Usuario


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuário / CPF / Matrícula',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu usuário'}),
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '••••••••'}),
    )


class CadastroCidadaoForm(forms.Form):
    first_name = forms.CharField(label='Nome', max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Sobrenome', max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Nome de usuário', max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefone = forms.CharField(label='Telefone', max_length=20, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(11) 99999-9999'}))
    password1 = forms.CharField(label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirmar senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    cpf = forms.CharField(label='CPF', max_length=14,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}))
    data_nascimento = forms.DateField(label='Data de nascimento', required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    endereco = forms.CharField(label='Endereço', max_length=300, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf'].replace('.', '').replace('-', '').strip()
        if not cpf.isdigit() or len(cpf) != 11:
            raise forms.ValidationError('CPF inválido. Use apenas 11 dígitos.')
        if Cidadao.objects.filter(_cpf=cpf).exists():
            raise forms.ValidationError('CPF já cadastrado.')
        return cpf

    def clean_username(self):
        username = self.cleaned_data['username']
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError('Nome de usuário já em uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('E-mail já cadastrado.')
        return email

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get('password1'), cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'As senhas não coincidem.')
        return cleaned

    def save(self):
        d = self.cleaned_data
        cidadao = Cidadao(
            username=d['username'],
            email=d['email'],
            first_name=d['first_name'],
            last_name=d['last_name'],
            tipo=Usuario.TIPO_CIDADAO,
            _cpf=d['cpf'],
            data_nascimento=d.get('data_nascimento'),
            endereco=d.get('endereco', ''),
        )
        cidadao._telefone = d.get('telefone', '')
        cidadao.set_password(d['password1'])
        cidadao.save()

        from solicitacoes.models import Historico
        Historico.objects.create(cidadao=cidadao)

        return cidadao


class CadastroServidorForm(forms.Form):
    first_name = forms.CharField(label='Nome', max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Sobrenome', max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Nome de usuário', max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefone = forms.CharField(label='Telefone', max_length=20, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirmar senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    matricula = forms.CharField(label='Matrícula funcional', max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    setor = forms.ChoiceField(label='Setor', choices=[
        ('Documentação', 'Documentação'),
        ('Agendamentos', 'Agendamentos'),
        ('Protocolos', 'Protocolos'),
        ('Atendimento Geral', 'Atendimento Geral'),
        ('Tributação', 'Tributação'),
        ('Saúde', 'Saúde'),
    ], widget=forms.Select(attrs={'class': 'form-select'}))
    cargo = forms.CharField(label='Cargo', max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    codigo_servidor = forms.CharField(label='Código de acesso servidor', max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Fornecido pela administração.')

    CODIGO_ACESSO = 'GOVFACIL2025'

    def clean_codigo_servidor(self):
        codigo = self.cleaned_data['codigo_servidor']
        if codigo != self.CODIGO_ACESSO:
            raise forms.ValidationError('Código de acesso inválido.')
        return codigo

    def clean_matricula(self):
        matricula = self.cleaned_data['matricula']
        if Servidor.objects.filter(matricula=matricula).exists():
            raise forms.ValidationError('Matrícula já cadastrada.')
        return matricula

    def clean_username(self):
        username = self.cleaned_data['username']
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError('Nome de usuário já em uso.')
        return username

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get('password1'), cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'As senhas não coincidem.')
        return cleaned

    def save(self):
        d = self.cleaned_data
        servidor = Servidor(
            username=d['username'],
            email=d['email'],
            first_name=d['first_name'],
            last_name=d['last_name'],
            tipo=Usuario.TIPO_SERVIDOR,
            matricula=d['matricula'],
            setor=d['setor'],
            cargo=d['cargo'],
        )
        servidor._telefone = d.get('telefone', '')
        servidor.set_password(d['password1'])
        servidor.save()
        return servidor
