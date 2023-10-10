Crie o app empresarial, onde os funcionários da empresa irão trabalhar:
```bash
python manage.py startapp empresarial
```

INSTALE O APP!

Crie a URL empresarial:
```bash
path('empresarial/', include('empresarial.urls')),
```

Em empresarial/urls.py crie:
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('gerenciar_clientes/', views.gerenciar_clientes, name="gerenciar_clientes"),
]
```

Crie a view gerenciar_clientes:
```bash
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Concat
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required 
def gerenciar_clientes(request):
    clientes = User.objects.filter(is_staff=False)

    nome_completo = request.GET.get('nome')
    email = request.GET.get('email')

    if email:
        clientes = clientes.filter(email__contains = email)
    if nome_completo:
        clientes = clientes.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        ).filter(full_name__contains=nome_completo)


    return render(request, 'gerenciar_clientes.html', {'clientes': clientes, 'nome_completo': nome_completo, 'email': email})
```

Desenvolva o HTML gerenciar_clientes:
```bash
{% extends "bases/base.html" %}
{% load static %}

{% block 'head' %}
    <link href="{% static 'exames/css/css.css' %}" rel="stylesheet">
    <link href="{% static 'exames/css/gerenciar_pedidos.css' %}" rel="stylesheet">
{% endblock 'head' %}


{% block 'conteudo' %}
    <br> 
    <br>
    <div class="container">
        {% if messages %}
            <br>
            {% for message in messages %}
            <div class="alert {{ message.tags }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
        <div class="row">
            <div class="col-md">
                <form action="{% url "gerenciar_clientes" %}" method="GET">
                <label for="">Nome</label>
                <input type="text" class="form-control" name="nome" value="{{nome_completo}}">
            </div>
            <div class="col-md">
                <label for="">E-mail</label>
                <input type="text" class="form-control" name="email" value="{{email}}">
            </div>
            <div class="col-md">
                <br>
                <input type="submit" class="btn-default">
                </form>

            </div>
        </div>
        <br>
        <div class="card card-view">
            <table>
                <tr>
                  <th>Nome</th>
                  <th>E-mail</th>
                  <th>CPF</th>
                </tr>

                {% for cliente in clientes %}
                    <tr class="linha-tabela">
                        <td><a href="#">{{cliente.get_full_name}}</a></td>
                        <td>{{cliente.email}}</td>
                        
                        <td>
                        
                        </td>
                    </tr>
                {% endfor %}
               
              </table>
              
            
        </div>

    </div>

{% endblock 'conteudo' %}
```

Crie a URL onde o admin irá acessar um paciente em específico:
```bash
path('cliente/<int:cliente_id>', views.cliente, name="cliente"),
```

Desenvolva a view:
```bash
@staff_member_required 
def cliente(request, cliente_id):
    cliente = User.objects.get(id=cliente_id)
    exames = SolicitacaoExame.objects.filter(usuario=cliente)
    return render(request, 'cliente.html', {'cliente': cliente, 'exames': exames})
```

Crie o HTML:
```bash
{% extends "bases/base.html" %}
{% load static %}

{% block 'head' %}
    <link href="{% static 'exames/css/css.css' %}" rel="stylesheet">
    <link href="{% static 'exames/css/gerenciar_pedidos.css' %}" rel="stylesheet">
    <link href="{% static 'exames/css/gerenciar_exames.css' %}" rel="stylesheet">
{% endblock 'head' %}


{% block 'conteudo' %}
    <br> 
    <br>
    <div class="container">
        {% if messages %}
            <br>
            {% for message in messages %}
            <div class="alert {{ message.tags }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
        <h3 class="font-destaque">{{cliente.get_full_name}}</h3>
        <p>{{cliente.email}}</p>
        <div class="card card-view">
            
            <div class="sub-card">
                <h3>Exames de sangue</h3>
                <hr>
                <br>
                {% for exame in exames  %}
                    {% if  exame.exame.tipo == 'S'%}
                        <div class="row">
                            <div class="col-md"><h3>{{exame.exame.nome}}</h3></div>
                            <div class="col-md">{{exame.badge_template}}</div>
                            <div class="col-md">
                                <a href="#" class="btn btn-light">Abrir</a>
                            </div>
                        </div>
                        <br>
                    {% endif %}
                {% endfor %}
            </div>
            <br>
            <br>
            <div class="sub-card">
                <h3>Exames de imagem</h3>
                <hr>
                <br>
                {% for exame in exames  %}
                    {% if  exame.exame.tipo == 'I'%}
                        <div class="row">
                            <div class="col-md"><h3>{{exame.exame.nome}}</h3></div>
                            <div class="col-md">{{exame.badge_template}}</div>
                            <div class="col-md"><a href="#" class="btn btn-light">Abrir</a></div>
                        </div>
                        <br>
                    {% endif %}
                {% endfor %}
            </div>
            
        </div>

    </div>

{% endblock 'conteudo' %}
```

Em gerenciar_clientes redirecione para tela do cliente:
```bash
<td><a href="{% url "cliente" cliente.id %}">{{cliente.get_full_name}}</a></td>
```
