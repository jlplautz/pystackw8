4RCrie a URL para usuarios:
```bash
path('usuarios/', include('usuarios.urls')),
```

Agora crie o arquivo urls.py dentro de usuarios:
```bash
from django.urls import path
from . import views
urlpatterns = [
    path('cadastro/', views.cadastro, name="cadastro"),
]
```

Crie a função cadastro em views.py:
```bash
def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
```

Configure onde o Django irá procurar por arquivos .html:
```bash
os.path.join(BASE_DIR, 'templates')
```

Crie o templates/bases/base.html:
```bash
{% load static %}
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VitaLab</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="st[+.lesheet">
{% block 'head' %}{% endblock %}
</FV head>
<body>
{% block 'conteudo' %}{% endblock %}
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
Agora vamos criar o cadastro.html
{% extends "bases/base.html" %}
{% load static %}
{% block 'head' %}
{% endblock 'head' %}
{% block 'conteudo' %}
PSW 8.0 | Aula 15<br>
<br>
<div class="container">
<h3 class="font-destaque">Cadastre-se</h3>
<div class="row">
<div class="col-md-3" style="text-align: center">
<img src="" alt="">
<h3>VitaLab</h3>
</div>
<div class="col-md-9">
<form action="" method="POST">
<label>Primeiro nome</label>
<br>
<input type="text" class="input-default" name="primeiro_nome">
<br>
<br>
<label>Último nome</label>
<br>
<input type="text" class="input-default" name="ultimo_nome">
</div>
</div>
<div class="row">
<div class="col-md-4">
<label>Username</label>
<br>
<input type="text" class="input-default w100" name="username">
<br>
<br>
<label>Senha</label>
<br>
<input type="text" class="input-default w100" name="senha">
</div>
<div class="col-md-4">
<label>E-mail</label>
<br>
<input type="text" class="input-default w100" name="email">
<br>
<br>
<label>Confirmar senha</label>
<br>
<input type="text" class="input-default w100" name="confirmar_senha">
</div>
</div>
<br>
<input type="submit" class="btn-default">
</form>
</div>
{% endblock %}
```

Nessa etapa, precisamos estilizar nossa aplicação criando os css. Para isso vamos configurar os arquivos estáticos:
```bash
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'templates/static'),)
STATIC_ROOT = os.path.join('static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

em templates/static/geral/css/base.css crie o arquivo:
```bash
:root{
--main-color: #151C34;
--dark-color: #0C121C ;
--light-color: #6DE6EE;
--contrast-color: #f4c96b;
--differential-color: #066668;
}
*{
PSW 8.0 | Aula 16color: white
}
.font-destaque{
color: var(--light-color);
font-size: 40px;
}
.input-default{
background-color: rgba(255,255,255,0.05);
border: 1px solid var(--differential-color);
padding: 7px;
width: 50%;
}
.w100{
width: 100%;
}
.btn-default{
background-color: var(--light-color);
color: black;
width: 15%;
padding: 10px;
border: none;
border-radius: 10px;
}
.font-destaque-secundaria{
color: var(--light-color);
font-size: 35px;
}
```

Agora é só importar o arquivo em base.html:
```bash
<link href="{% static 'geral/css/base.css' %}" rel="stylesheet">
Crie o arquivo templates/static/usuarios/css/css.css:
body{
background-image: url('/static/geral/img/bg1.png');
background-size: cover;
}
p{
color: var(--light-color);
}
```

Ficou faltando a imagem, adicione a imagem ‘bg1.png’ dentro de templates/static/geral/img/bg1.png
Imagens para download 👇
Acesse pelo NOTION para realizar o download das imagens, link no início do PDF:
bg1.png
bg2.png
logo.png


Importe o css de cadastro:
```bash
<link href="{% static 'usuarios/css/css.css' %}" rel="stylesheet">
```

Adicione a logo da empresa:
```bash
<img src="{% static 'geral/img/logo.png' %}" alt="">
```

Execute as migrações:
```bash
python manage.py makemigrations
python manage.py migrate
```

Crie as funcionalidades de cadastro na view:
```bash
def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        if not senha == confirmar_senha:
            return redirect('/usuarios/cadastro')
        if len(senha) < 6:
            return redirect('/usuarios/cadastro')
        try:
            # Username deve ser único!
            user = User.objects.create_user(
            first_name=primeiro_nome,
            last_name=ultimo_nome,
            username=username,
            email=email,
            password=senha,
        )
    except:
        return redirect('/usuarios/cadastro')
    return redirect('/usuarios/cadastro')
```

Altere o form para enviar os dados para a view:
```bash
<form action="{% url 'cadastro' %}" method="POST"> {% csrf_token %}
```
Configure o Django message em settings.py:
```bash
PSW 8.0 | Aula 18from django.contrib.messages import constants
MESSAGE_TAGS = {
    constants.DEBUG: 'alert-primary',
    constants.ERROR: 'alert-danger',
    constants.WARNING: 'alert-warning',
    constants.SUCCESS: 'alert-success',
    constants.INFO: 'alert-info',
}
```

Agora adicione as mensagens nos pontos estratégicos do código:
```bash
messages.add_message(request, constants.ERROR, 'As senhas não coincidem')
```

Exiba as mensagens no HTML de cadastro:
```bash
{% if messages %}
    <br>
    {% for message in messages %}
    <div class="alert {{ message.tags }}">{{ message }}</div>
    {% endfor %}
{% endif %}
```

