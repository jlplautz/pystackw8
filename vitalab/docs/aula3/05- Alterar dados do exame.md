Exiba dinamicamente o status e o check do exame:
```bash
<select name="status" id="" class="form-select">
    <option style="color: black;" {% if exame.status == "E" %}selected{% endif %} value="E">Em análise</option>
    <option style="color: black;" {% if exame.status == "F" %}selected{% endif %} value="F">Finalizado</option>
</select>
```
```bash
<input type="checkbox" name="requer_senha" id="" {% if exame.requer_senha %}checked{% endif %}><label for="">Requer senha para acessar ?</label>
```

Altere o form para enviar dados para URL:
```bash
<form action="{% url "alterar_dados_exame" exame.id %}" method="POST" enctype="multipart/form-data">{% csrf_token %}
```

Crie a URL:
```bash
path('alterar_dados_exame/<int:exame_id>', views.alterar_dados_exame, name="alterar_dados_exame"),
```

E crie a VIEW:
```bash
@staff_member_required 
def alterar_dados_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)

    pdf = request.FILES.get('resultado')
    status = request.POST.get('status')
    requer_senha = request.POST.get('requer_senha')
    
    if requer_senha and (not exame.senha):
        messages.add_message(request, constants.ERROR, 'Para exigir a senha primeiro crie uma.')
        return redirect(f'/empresarial/exame_cliente/{exame_id}')
    
    exame.requer_senha = True if requer_senha else False

    if pdf:
        exame.resultado = pdf
        
    exame.status = status
    exame.save()
    messages.add_message(request, constants.SUCCESS, 'Alteração realizada com sucesso')
    return redirect(f'/empresarial/exame_cliente/{exame_id}')
```
