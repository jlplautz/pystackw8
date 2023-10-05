Crie uma URL para o app exames:
```bash
path('exames/', include('exames.urls')),
```

Crie o arquivo urls.py em exames:
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('solicitar_exames/', views.solicitar_exames, name="solicitar_exames"),
]
```
Agora vamos para view solicitar_exames:
```bash
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def solicitar_exames(request):
    if request.method == "GET":
        return render(request, 'solicitar_exames.html')
```

Dentro de exames/templates crie o solicitar_exames.html:
```bash
{% extends "bases/base.html" %}
{% load static %}

{% block 'head' %}
    
{% endblock 'head' %}

{% block 'conteudo' %}
    <br>
    <br>
    <div class="container">
        <div class="row">

            <div class="col-md">
                <h3 class="font-destaque">Solicitar exames</h3>
                
                <form action="" method="POST">
                    <label for="">Selecione os exames para realizar</label>
                    <select class="select form-control bg-select" multiple name="exames">
                       
                            <option class="opt" value="">Exame 1</option>
                        
                    </select>
                    <br>
                    <input  type="submit" class="btn-default tamanho-2"  name="ultimo_nome" value="Solicitar exames">
                </form>
            </div>

            <div class="col-md-2">

            </div>

            <div class="col-md card">
    
                        <div style="font-size: 20px; font-weight: bold">
                           
                            <img src="{% static 'exames/img/check.png' %}">
                            
                            Exame 1
                            <span class="previa-preco">
                               R$ 30
                            </span>
                        </div>
                   
                    
                    <hr style="color: white;">
                    <div>
                        <label>Total: </label><label class="previa-preco">R$ 30</label>
                    </div>
                    <br>

                    <h5>Data: 08 de Setembro</h5>
                    <br>

                    <form action="" method="POST">
                        <button class="btn-secundario">Fechar pedido</button>
                    </form>
                    
              

            </div>
        </div>
    </div>

{% endblock 'conteudo' %}
```

Crie o arquivo css.css de exames nos arquivos estáticos:
```bash
body{

    background-image: url('/static/geral/img/bg2.png');
    background-size: cover;

}


.bg-select{
    background-color: transparent;
    border-color: var(--differential-color);
}

.card{
    background-color: rgba(217, 217, 217, .14);
    color: white;
    padding: 15px;
}

.previa-preco{
    float: right;
    font-weight: bold;
}

.tamanho-2{
    width: 50%;
}

.btn-secundario{

    background-color: #838FFF;
    color: black;
    padding: 10px;
    font-weight: bold;
    border: none;
    border-radius: 10px;
}

.btn-secundario-outline{
    background-color: transparent;
    border-color: #838FFF;
    padding: 10px;
}
```
Importe o arquivo em solicitar_exame.htm
```bash
<link href="{% static 'exames/css/css.css' %}" rel="stylesheet">
```
Para listar dinamicamente os exames, busque todos os tipos nas views:
```bash
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import TiposExames

@login_required
def solicitar_exames(request):
    tipos_exames = TiposExames.objects.all()
    if request.method == "GET":
        return render(request, 'solicitar_exames.html', {'tipos_exames': tipos_exames})
```
Exiba dinamicamente no HTML as opções selecionáveis dos exames:
```bash
{% for exame in tipos_exames %}
    <option class="opt" value="{{exame.id}}">{{exame}}</option>
{% endfor %}
```

Atualize o form para enviar os dados para solicitar_exames:
```bash
<form action="{% url "solicitar_exames" %}" method="POST">{% csrf_token %}
```

Atualize a view para processar a requisição POST:
```bash
@login_required
def solicitar_exames(request):
    tipos_exames = TiposExames.objects.all()
    if request.method == "GET":
        return render(request, 'solicitar_exames.html', {'tipos_exames': tipos_exames})
    else:
        exames_id = request.POST.getlist('exames')

        solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)
        #preco_total = solicitacao_exames.aggregate(total=Sum('preco'))['total']
        preco_total = 0
        for i in solicitacao_exames:
            preco_total += i.preco
        
        return render(request, 'solicitar_exames.html', {'solicitacao_exames': solicitacao_exames, 'preco_total': preco_total, 'tipos_exames': tipos_exames})
```

Exiba os dados do pedido dinamicamente para o cliente aprovar:
```bash
{% if solicitacao_exames %}

    {% for exame in solicitacao_exames %}
        <div style="font-size: 20px; font-weight: bold">
            {% if exame.disponivel %}
                <img src="{% static 'exames/img/check.png' %}">
            {% else %}
                <img src="{% static 'exames/img/exit.png' %}">
            {% endif %}
            {{exame.nome}}
            <span class="previa-preco">
                {{exame.preco}}
            </span>
        </div>
    {% endfor %}
    
    <hr style="color: white;">
    <div>
        <label>Total: </label><label class="previa-preco">{{preco_total}}</label>
    </div>
    <br>

    <h5>Data: 08 de Setembro</h5>
    <br>

    <form action="{% url "fechar_pedido" %}" method="POST">{% csrf_token %}
        {% for exame in solicitacao_exames  %}
            <input type="hidden" value="{{exame.id}}" name="exames">
        {% endfor %}
        <button class="btn-secundario">Fechar pedido</button>
    </form>
    
{% else %}
    <h3>Nenhum exame selecionado</h3>
{% endif %}
```
Adicione as imagens nos arquivos estáticos:
```bash

```
Agora adicione os exames solicitados em um input hidde:
```bash
{% for exame in solicitacao_exames  %}
    <input type="hidden" value="{{exame.id}}" name="exames">
{% endfor %}
```

Crie a URL para fechar o pedido:
```bash
path('fechar_pedido/', views.fechar_pedido, name="fechar_pedido"),
```
Crie a view para fechar o pedido do cliente:
```bash
@login_required
def fechar_pedido(request):
    exames_id = request.POST.getlist('exames')
    solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)

    pedido_exame = PedidosExames(
        usuario = request.user,
        data = datetime.now()
    )

    pedido_exame.save()

    for exame in solicitacao_exames:
        solicitacao_exames_temp = SolicitacaoExame(
            usuario=request.user,
            exame=exame,
            status="E"
        )
        solicitacao_exames_temp.save()
        pedido_exame.exames.add(solicitacao_exames_temp)
        
    pedido_exame.save()

    messages.add_message(request, constants.SUCCESS, 'Pedido de exame concluído com sucesso')
    return redirect('/exames/ver_pedidos/')
```

Redirecione o form para o fechar_pedido:
```bash
<form action="{% url "fechar_pedido" %}" method="POST">{% csrf_token %}
```
