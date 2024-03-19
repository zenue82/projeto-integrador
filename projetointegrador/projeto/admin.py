from django.contrib import admin
from .models import Mensagem

class MensagemAdmin(admin.ModelAdmin):
    list_display = ['id', 'texto', 'remetente', 'chat', 'data_envio']  # Substitua 'assunto' e 'destinatario' pelos campos corretos da sua classe Mensagem

admin.site.register(Mensagem, MensagemAdmin)
