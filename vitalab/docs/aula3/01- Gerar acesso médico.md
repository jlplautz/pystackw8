Crie a model onde iremos armazenar os links de acessos médicos:
```bash
class AcessoMedico(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    identificacao = models.CharField(max_length=50)
    tempo_de_acesso = models.IntegerField() # Em horas
    criado_em = models.DateTimeField()
    data_exames_iniciais = models.DateField()
    data_exames_finais = models.DateField()
    token = models.CharField(max_length=20)

    def __str__(self):
        return self.token
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = token_urlsafe(6)

        super(AcessoMedico, self).save(*args, **kwargs)
```

Execute as migrações e cadastre no ADMIN!
```bash
path('gerar_acesso_medico/', views.gerar_acesso_medico, name="gerar_acesso_medico"),
```

Crie a view:
```bash
@login_required
def gerar_acesso_medico(request):
    if request.method == "GET":
        acessos_medicos = AcessoMedico.objects.filter(usuario =request. user)
        return render(request, 'gerar_acesso_medico.html', {'acessos_medicos': acessos_medicos})
    elif request.method == "POST":
        identificacao = request.POST.get('identificacao')
        tempo_de_acesso = request.POST.get('tempo_de_acesso')
        data_exame_inicial = request.POST.get("data_exame_inicial")
        data_exame_final = request.POST.get("data_exame_final")

        acesso_medico = AcessoMedico(
            usuario = request.user,
            identificacao = identificacao,
            tempo_de_acesso = tempo_de_acesso,
            data_exames_iniciais = data_exame_inicial,
            data_exames_finais = data_exame_final,
            criado_em = datetime.now()
        )

        acesso_medico.save()

        messages.add_message(request, constants.SUCCESS, 'Acesso gerado com sucesso')
        return redirect('/exames/gerar_acesso_medico')
```

Crie o HTML gerar_acesso_medico:
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
            <div class="col-md-5">
                <h3>Gerar acesso médico</h3>

                <form action="{% url "gerar_acesso_medico" %}" method="POST">{% csrf_token %}

                    <label for="">Identificação</label>
                    <br>
                    <input style="width: 100%" type="text" name="identificacao" id="" class="input-default">
                    <br>
                    <br>
                    <label for="">Tempo de acesso (em horas)</label>
                    <br>
                    <input style="width: 100%" type="number" name="tempo_de_acesso" id="" class="input-default">
                    <br>
                    <br>
                    <div class="row">
                        <label for="">Acesso a exames realizados entre:</label>
                        <div class="col-md">
                            <input style="width: 100%" type="date" name="data_exame_inicial" id="" class="input-default">
                        </div>
                        <div class="col-md">
                            <input style="width: 100%" type="date" name="data_exame_final" id="" class="input-default">
                            <br>
                            <br>
                        </div>
                   
                        
                    </div>
                    <input style="width: 40%" type="submit" class="btn-default" value="Gerar link">
                </form>
            </div>
            <div class="col-md">
                
                <div class="card">
                    <table style="text-align: center">
                        <tr>
                          <th>Id</th>
                          <th>Status</th>
                          <th>Link</th>
                          
                        </tr>
        
                       
                            <tr class="linha-tabela">
                                <td>01</td>
                                <td>Status 1</td>
                                <td>URL AQUI</td>
                            </tr>
                      
                    
                       
                    </table>
                </div>

            </div>
        </div>
    </div>
{% endblock 'conteudo' %}
```

Exiba os acesso dinamicamente:
```bash
{% for acesso in acessos_medicos  %}
    <tr class="linha-tabela">
        <td>{{acesso.identificacao}}</td>
        <td>{{acesso.status}}</td>
        <td><a href="{{acesso.url}}">{{acesso.url}}</a></td>
    </tr>
{% endfor %}
```

Crie os métodos da model:
```bash
@property
    def status(self):
        return 'Expirado' if timezone.now() > (self.criado_em + timedelta(hours=self.tempo_de_acesso)) else 'Ativo'
  
@property
def url(self):
    #TODO: reverse
    return f"http://127.0.0.1:8000/exames/acesso_medico/{self.token}"
```

Crie a URL onde o médico irá acessar:
```bash
path('acesso_medico/<str:token>', views.acesso_medico, name="acesso_medico"),
```

Crie a view:
```bash
def acesso_medico(request, token):
    acesso_medico = AcessoMedico.objects.get(token = token)

    if acesso_medico.status == 'Expirado':
        messages.add_message(request, constants.WARNING, 'Esse link já se expirou!')
        return redirect('/usuarios/login')

    pedidos = PedidosExames.objects.filter(data__gte = acesso_medico.data_exames_iniciais).filter(data__lte = acesso_medico.data_exames_finais).filter(usuario=acesso_medico.usuario)

    return render(request, 'acesso_medico.html', {'pedidos': pedidos})
```

Por fim, crie o HTML do médico:
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

        
        <table style="">
            <tr>
              <th>Id</th>
              <th>Exame</th>
              
            </tr>
						<tr class="linha-tabela">
	            <td>Nome</td>
	            
	            
	               <td>Em análise</td>
	            
	        </tr>
           
           
        </table>
    </div>
{% endblock 'conteudo' %}
```

Liste dinamicamente os exames:
```bash
 {% for pedido in pedidos %}
    {% for exame in pedido.exames.all %}
        <tr class="linha-tabela">
            <td>{{exame.exame.nome}}</td>
            
            {% if exame.resultado %}
                <td><a style="text-decoration: none;" class="btn-secundario" href="{{exame.resultado.url}}">Ver exame</a></td>
            {% else %}
                <td>Em análise</td>
            {% endif %}
        </tr>
    {% endfor %}
{% endfor %}
```
