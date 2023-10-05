Agora vamos trabalhar com o gerenciamento dos pedidos de exames.
```bash
path('gerenciar_pedidos/', views.gerenciar_pedidos, name="gerenciar_pedidos"),
```

Crie a view para exibir a página HTML
```bash
@login_required
def gerenciar_pedidos(request):
    pedidos_exames = PedidosExames.objects.filter(usuario=request.user)
    return render(request, 'gerenciar_pedidos.html', {'pedidos_exames': pedidos_exames})
```

Crie o HTML gerenciar_pedidos:
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
        <div class="card card-view">
            <table>
                <tr>
                  <th>Solicitação</th>
                  <th>Data</th>
                  <th>Exames</th>
                  <th>Ação</th>
                </tr>

                {% for pedidos in pedidos_exames %}
                    <tr class="linha-tabela">
                        <td>{{pedidos.id}}</td>
                        <td>{{pedidos.data}}</td>
                        <td>
                            <select class="form-select">
                                {% for exame in pedidos.exames.all %}
                                    <option style="color: black"  value="">{{exame.exame.nome}}</option>
                                {% endfor %}
                            </select>
                        </td>
                        <td>
                         
                            <a href=""  class="btn btn-danger {% if not pedidos.agendado %} disabled {% endif %}">Cancelar</a>
                        </td>
                    </tr
                {% endfor %}
               
              </table>
              
            
        </div>

    </div>

{% endblock 'conteudo' %}
```

Crie o CSS gerenciar_pedidos.css:
```bash
.linha-tabela{
    background-color: var(--dark-color);
    height: 20px;
}

td, th{
    padding: 20px;
}

.card-view{
    text-align: center;
    padding: 0;
    border: none;
    height: 70vh;
}
```

Em urls.py de exames crie a URL responsável por cancelar o pedido:
```bash
path("cancelar_pedido/<int:pedido_id>", views.cancelar_pedido, name="cancelar_pedido"),
```

Crie a view cancelar_pedido:
```bash
@login_required
def cancelar_pedido(request, pedido_id):
    pedido = PedidosExames.objects.get(id=pedido_id)

    if not pedido.usuario == request.user:
        messages.add_message(request, constants.ERROR, 'Esse pedido não é seu')
        return redirect('/exames/gerenciar_pedidos/')

    pedido.agendado = False
    pedido.save()
    messages.add_message(request, constants.SUCCESS, 'Pedido excluido com sucesso')
    return redirect('/exames/gerenciar_pedidos/')
```

Por questões de segurança realize a verificação se o pedido é realmente do usuário logado:
```bash
if not pedido.usuario == request.user:
      messages.add_message(request, constants.ERROR, 'Esse pedido não é seu')
      return redirect('/exames/gerenciar_pedidos/')
```

Altere o botão de cancelar pedido para:
```bash
<a href="{% url "cancelar_pedido" pedidos.id %}"  class="btn btn-danger {% if not pedidos.agendado %} disabled {% endif %}">Cancelar</a>
```
