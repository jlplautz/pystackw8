from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.shortcuts import redirect, render


def cadastro(request):
    if request.method == 'GET':
        return render(request, 'usuarios/cadastro.html')
    else:
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(
                request,
                constants.ERROR,
                'As senhas não coincidem',
            )
            return redirect('/usuarios/cadastro')

        if len(senha) < 6:
            messages.add_message(
                request,
                constants.ERROR,
                'Sua senha deve ter mais de 6 caracteres',
            )
            return redirect('/usuarios/cadastro')

        if User.objects.filter(username=username).exists():
            messages.add_messages(
                request,
                constants.ERROR,
                'Já existe um com este Username.',
            )
            return redirect('/usuarios/cadastro')

        try:
            user = User.objects.create_user(
                first_name=primeiro_nome,
                last_name=ultimo_nome,
                username=username,
                email=email,
                password=senha,
            )
        except Exception:
            return redirect('/usuarios/cadastro')

        return redirect('/usuarios/cadastro')


def logar(request):
    if request.method == 'GET':
        return render(request, 'usuarios/login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        user = authenticate(username=username, password=senha)
        if user:
            login(request, user)
            # Acontecerá um erro ao redirecionar por enquanto,
            # resolveremos nos próximos passos
            return redirect('/usuarios/login')
        else:
            messages.add_message(
                request,
                constants.ERROR,
                'Usuario ou senha inválidos',
            )
        return redirect('/usuarios/login')
