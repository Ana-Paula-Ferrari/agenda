from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

from core.models import Evento

# Create your views here.

#def index(request):
 #  return redirect('/agenda') #vai redirecionar para a página agenda

def login_user(request): #usuario está logado
   return render(request, 'login.html') #mostrara a pág de login


def logout_user(request): #encerrar a sessão
   logout(request)
   return redirect('/')


def submit_login(request):
   if request.POST:
     username = request.POST.get('username') #Recuperar a informação do formulário
     password = request.POST.get('password')
     usuario = authenticate(username=username, password=password)
     if usuario is not None:
      login(request, usuario)
      return redirect('/')
     else:
      messages.error(request, "Usuário ou senha inválido!") #Vai enviar uma mensagem para login.html-
   return redirect('/')



@login_required(login_url='/login/')#Validar autenticação
def lista_eventos(request):   
   usuario = request.user
   # evento = Evento.objects.get(id=1) #Consultar id
   #evento = Evento.objects.all() #Listar todos os dados
   data_atual = datetime.now() - timedelta(hours=1) #data atual/ mostrar evento que passou até 1 hora
   evento = Evento.objects.filter(usuario=usuario,
                                  data_evento__gt=data_atual) #Filtrar eventos do usuario da data atual em diante __gt/ menor que a data atual __lt
   dados = {'eventos':evento}
   return render(request,'agenda.html', dados)



@login_required(login_url='/login/') 
def evento(request):
   id_evento = request.GET.get('id')
   dados = {} #Caso não encontre o id retornar o dicionário vazio
   if id_evento: #Se tiver o id passar os eventos
      dados['evento'] = Evento.objects.get(id=id_evento)
   return render(request, 'evento.html', dados)



@login_required(login_url='/login')
def submit_evento(request):
   if request.POST:
      titulo = request.POST.get('titulo')
      data_evento = request.POST.get('data_evento')
      descricao = request.POST.get('descricao')
      usuario = request.user #pegar inforações do usuário
      id_evento = request.POST.get('id_evento')

      #Caso de alteração/edição dos dados
      #if id_evento:
         #Evento.objects.filter(id=id_evento).update( titulo=titulo,
                                                     # data_evento=data_evento,
                                                      #descricao=descricao)

      #Caso de alteracao/edição dos dados com validação do usuário
      if id_evento:
         evento = Evento.objects.get(id=id_evento)
         if evento.usuario == usuario:
            evento.titulo = titulo
            evento.descricao = descricao
            evento.data_evento = data_evento
            evento.save()
            
      #Caso de inserção dos dados
      else:
         Evento.objects.create(titulo=titulo,
                              data_evento=data_evento,
                              descricao=descricao,
                              usuario=usuario)
   return redirect('/')



@login_required(login_url='/login/')
def delete_evento(request, id_evento):
   #Cada usuario podera excluir o evento que é dele
   usuario = request.user
   try:
      evento = Evento.objects.get(id=id_evento) #Vai buscar na tabelas o id do evento
   except Exception:
      raise Http404()
   if usuario == evento.usuario: #Verificar se o usuario que esta logado é o que criou o id
      evento.delete()  #Deletar o registro 
   else:
      raise Http404()
   return redirect('/')



#@login_required(login_url='/login/')
#def json_lista_evento(request):
  # usuario = request.user
  # evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo') #Valores a ser exibido
  # return JsonResponse(list(evento), safe=False) #Lista de ids e titulos/ safe necessário porque está passando lista e não dicionário

#Deixar a informacoes da agenda dispónivel
def json_lista_evento(request, id_usuario):
   usuario = User. objects.get(id=id_usuario)
   evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')
   return JsonResponse(list(evento), safe=False)
