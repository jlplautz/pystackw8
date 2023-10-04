Login
Crie uma URL para login:
```bash
path('login/', views.logar, name="login"),
```

Crie a view logar:
```bash
def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        user = authenticate(username=username, password=senha)
    if user:
        login(request, user)
        # Acontecerá um erro ao redirecionar por enquanto, resolveremos nos próximos passos
        return redirect('/')
    else:
        messages.add_message(request, constants.ERROR, 'Usuario ou senha inválidos')
        return redirect('/usuarios/login')
```

Crie o login.html:
```bash
{% extends "bases/base.html" %}
{% load static %}
{% block 'head' %}
    <link href="{% static 'usuarios/css/css.css' %}" rel="stylesheet">
{% endblock 'head' %}
{% block 'conteudo' %}
    <div class="container">
        <h3 class="font-destaque-secundaria"> <img width="10%" src="{% static 'geral/img/logo.png' %}" alt="">Cadastre-se</h3>
    {% if messages %}
        <br>
        {% for message in messages %}
            <div class="alert {{ message.tags }}">{{ message }}</div>
        {% endfor %}
    {% endif %}
    <div>
        <form action="{% url 'login' %}" method="POST">{% csrf_token %}
        <label>Username</label>
        <br>
        <input type="text" class="input-default" name="username">
        <br>
        <br>
        <label>Senha</label>
        <br>
        <input type="text" class="input-default" name="senha">
        <br>
        <br>
        <input type="submit" class="btn-default" value="Logar">
        </form>
    </div>
</div>
{% endblock %}
```
