
Nessa etapa iremos gerenciar individualmente os exames do cliente.

Crie a URL gerenciar_exame:
```bash
path('gerenciar_exames/', views.gerenciar_exames, name="gerenciar_exames"),
```

Agora a view:
```bash
@login_required
def gerenciar_exames(request):
    exames = SolicitacaoExame.objects.filter(usuario=request.user)

    return render(request, 'gerenciar_exames.html', {'exames': exames})
```

Crie o HTML gerenciar_exames:
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
        <div class="card card-view">
            
            <div class="sub-card">
                <h3>Exames de sangue</h3>
                <hr>
                <br>
                LISTAR EXAMES AQUI
            </div>
            <br>
            <br>
            <div class="sub-card">
                <h3>Exames de imagem</h3>
                <hr>
                <br>
                LISTAR EXAMES AQUI
            </div>
            
        </div>

    </div>

{% endblock 'conteudo' %}
```

Crie o gerenciar_exames.css
```bash
.sub-card{
    background-color: var(--dark-color);
    padding: 20px;
}
```

Liste os exames de sangue:
```bash
{% for exame in exames  %}
    {% if  exame.exame.tipo == 'S'%}
        <div class="row">
            <div class="col-md"><h3>{{exame.exame.nome}}</h3></div>
            <div class="col-md">{{exame.badge_template}}</div>
            <div class="col-md">
                {% if exame.status == 'F' %}
                    <a href="{% url "permitir_abrir_exame" exame.id %}" class="btn btn-light">Abrir</a>
                {% else %}
                    <a href="#" class="btn btn-light disabled">Abrir</a>
                {% endif %}
            </div>
        </div>
        <br>
    {% endif %}
{% endfor %}
```

Liste os exames de imagens:
```bash
{% for exame in exames  %}
    {% if  exame.exame.tipo == 'I'%}
        <div class="row">
            <div class="col-md"><h3>{{exame.exame.nome}}</h3></div>
            <div class="col-md">{{exame.badge_template}}</div>
            <div class="col-md">
                {% if exame.status == 'F' %}
                    <a href="{% url "permitir_abrir_exame" exame.id %}" class="btn btn-light">Abrir</a>
                {% else %}
                    <a href="#" class="btn btn-light disabled">Abrir</a>
                {% endif %}
        </div>
        <br>
    {% endif %}
{% endfor %}
```

Em SolicitacaoExame crie o badge_template:
```bash
from django.utils.safestring import mark_safe

def badge_template(self):
	if self.status == 'E':
	    classes_css = 'bg-warning text-dark'
	    texto = "Em análise"
	elif self.status == 'F':
	    classes_css = 'bg-success'
	    texto = "Finalizado"
	
	return mark_safe(f"<span class='badge bg-primary {classes_css}'>{texto}</span>")
```

Agora crie uma URL para permitir que o exame seja aberto:
```bash
path('permitir_abrir_exame/<int:exame_id>', views.permitir_abrir_exame, name="permitir_abrir_exame"),
```

Crie a view permitir_abrir_exame:
```bash
@login_required
def permitir_abrir_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
		#TODO: validar se o exame é do usuário
    if not exame.requer_senha:
        # verificar se o pdf existe
        return redirect(exame.resultado.url)

    else: 
        return redirect(f'/exames/solicitar_senha_exame/{exame.id}')
```

Altere os botões abrir para:
```bash
<a href="{% url "permitir_abrir_exame" exame.id %}" class="btn btn-light">Abrir</a>
```

No core do projeto adicione a URL de media ao urlpatterns:
```bash
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('exames/', include('exames.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Vamos para url que solicita a senha do exame:
```bash
path('solicitar_senha_exame/<int:exame_id>', views.solicitar_senha_exame, name="solicitar_senha_exame"),
```

Crie a view responsável:
```bash
@login_required
def solicitar_senha_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
    if request.method == "GET":
        return render(request, 'solicitar_senha_exame.html', {'exame': exame})
    elif request.method == "POST":
        senha = request.POST.get("senha")
				#TODO: validar se o exame é do usuário
        if senha == exame.senha:
            return redirect(exame.resultado.url)
        else:
            messages.add_message(request, constants.ERROR, 'Senha inválida')
            return redirect(f'/exames/solicitar_senha_exame/{exame.id}')
```

Crie o HTML solicitar_senha_exame:
```bash
{% extends "bases/base.html" %}
{% load static %}

{% block 'head' %}
    <link href="{% static 'exames/css/css.css' %}" rel="stylesheet">
    <link href="{% static 'exames/css/gerenciar_pedidos.css' %}" rel="stylesheet">
    <link href="{% static 'exames/css/gerenciar_exames.css' %}" rel="stylesheet">
{% endblock 'head' %}


{% block 'conteudo' %}
    <br><br>
    
    <div class="container">
        {% if messages %}
            <br>
            {% for message in messages %}
            <div class="alert {{ message.tags }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
        <h3>{{exame.exame.nome}}</h3>
        <br>
        <form action="{% url "solicitar_senha_exame" exame.id %}" method="POST">{% csrf_token %}
            
            <label>Senha de acesso</label>
            <br>
            <input type="text" name="senha" class="form-control" style="width: 40%">
            <br>

            <input type="submit" class="btn-default">
            
        </form>
        
    </div>

{% endblock 'conteudo' %}
```
