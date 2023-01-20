from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Estrutura para criar a tabela
class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True,null=True)
    data_evento = models.DateTimeField(verbose_name='Data do Evento')#Customizar o nome
    data_criacao = models.DateField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)#Se o usuario for excluido, todos os eventos pertencente a ele também são
    
    
    
  
    class Meta:
        db_table='evento' #Força o nome da tabela ser evento
    
   
   
   
    #Como o admin vai tratar esse objeto
    def __str__(self):
        return self.titulo #Vai retornar o nome dado no titulo