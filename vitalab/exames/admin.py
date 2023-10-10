from django.contrib import admin

from .models import AcessoMedico, PedidosExames, SolicitacaoExame, TiposExames

admin.site.register(TiposExames)
admin.site.register(PedidosExames)
admin.site.register(SolicitacaoExame)
admin.site.register(AcessoMedico)
