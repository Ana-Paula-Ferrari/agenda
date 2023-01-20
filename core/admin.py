from django.contrib import admin
from core.models import Evento

# Register your models here.

class EventoAdmin(admin.ModelAdmin): #Listagem no Admin _ class de administração
    list_display = ('titulo','data_evento','data_criacao') #Campos que quero que apareça
    list_filter = ('usuario','data_evento',) #virgula tem que estar no final/ cria um filtro no admin

admin.site.register(Evento, EventoAdmin) #Associar a tabela a listagem