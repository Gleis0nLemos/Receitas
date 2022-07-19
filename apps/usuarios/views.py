from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita

def cadastro(request):
    '''Cadastra um novo usuário no site.'''
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']

        if campo_vazio(nome):
            messages.error(request, 'Campo nome está vazio.')
            return redirect('cadastro')

        if campo_vazio(email):
            messages.error(request, 'Endereço de email inválido!')
            return redirect('cadastro')

        if senhas_diferentes(senha, senha2):
            messages.error(request, 'As senhas não coincidem!')
            return redirect('cadastro')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado.')
            return redirect('cadastro')

        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Email já cadastrado.')
            return redirect('cadastro')

        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('login')
        
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    '''Realiza o login de usuários cadastrados, com email e senha.'''
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']

        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'Preencha os campos corretamente.')
            return redirect('login')
        print(email, senha)

        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('dashboard')

    return render(request, 'usuarios/login.html')

def logout(request):
    '''Desloga o usuário do sistema.'''
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    '''Mostra o crud de receitas criadas pelo próprio usuário.'''
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-date_receita').filter(pessoa=id)

        dados = { 
            'receitas' : receitas
        }
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')

'''Abaixo, verificações usadas para cadastro e login.'''
def campo_vazio(campo):
    return not campo.strip()

def senhas_diferentes(senha, senha2):
    return senha != senha2

