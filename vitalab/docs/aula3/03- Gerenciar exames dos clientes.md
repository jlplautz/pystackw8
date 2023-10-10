Crie a URL:
```bash
path('exame_cliente/<int:exame_id>', views.exame_cliente, name="exame_cliente"),
```

Crie a view exame_cliente:
```bash
@staff_member_required 
def exame_cliente(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
    return render(request, 'exame_cliente.html', {'exame': exame})
```

Crie o HTML exame_cliente.html
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
    <div class="container">
        {% if messages %}
            <br>
            {% for message in messages %}
            <div class="alert {{ message.tags }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
        <div class="row">
        <h3 class="font-destaque">{{exame.usuario.get_full_name}}</h3>
        <p>{{exame.usuario.email}}</p>
        <br>
        <div class="row">
            <div class="col-md-6">
                <form action="" method="POST">
                    <input type="FILE" value="Alterar PDF" class="btn-secundario" name="resultado">
               
                    <br>
                    <br>
                    {% if exame.resultado %}
                        <a style="width: 100%;" href="" target="__blank"><div  style="width: 100%;" id="pdf-container">Seu exame aqui</div></a>
                    {% endif %}
            </div>
            <div class="col-md-6">
                <h3>Status</h3>

                <select name="status" id="" class="form-select">
                    <option style="color: black;" value="E">Em análise</option>
                    <option style="color: black;" value="F">Finalizado</option>
                </select>
                <br>
                <input type="checkbox" name="requer_senha" id=""><label for="">Requer senha para acessar ?</label>
                <br>
                <br>

                <input type="submit" value="Salvar" class="btn-default">
                </form>
                <a style="text-decoration: none;" href="" class="btn-secundario">Gerar senha</a>
            </div>
        </div>
        
    </div>

{% endblock 'conteudo' %}
```

Em cliente.html redirecione para a nova URL:
```bash
<a href="{% url "exame_cliente" exame.id %}" class="btn btn-light">Abrir</a>
```

Para exibir o PDF do exame valor utilizar um JavaScript:
```bash
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/pdf.min.js"></script>
<script>

    const container = document.getElementById('pdf-container');

    pdfjsLib.getDocument('').promise.then(pdf => {
        pdf.getPage(1).then(page => {
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            const viewport = page.getViewport({ scale: 0.6 });

            canvas.width = viewport.width;
            canvas.height = viewport.height;

            page.render({ canvasContext: context, viewport }).promise.then(() => {
                container.appendChild(canvas);
            });
        });
    });
</script>
```

Para funcionar crie a proxy_pdf:
```bash
path('proxy_pdf/<int:exame_id>', views.proxy_pdf, name="proxy_pdf"),
```

E sua respectiva VIEW:
```bash
@staff_member_required 
def proxy_pdf(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)

    response = exame.resultado.open()
    return FileResponse(response)
```
