from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Chat, Mensagem
from .forms import MensagemForm
from django.contrib.auth import views as auth_views  # Importe as views de autenticação
from django.http import JsonResponse
from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redireciona para a página de login após o registro bem-sucedido
    else:
        form = UserCreationForm()
    return render(request, 'comunicacao/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redireciona para a página de perfil após a atualização bem-sucedida
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'form': form})


@login_required
def enviar_mensagem(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.method == 'POST':
        form = MensagemForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                mensagem = form.save(commit=False)
                mensagem.remetente = request.user
                mensagem.chat = chat
                mensagem.save()
            # Envio de mensagem para o grupo do chat usando Channels
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"chat_{chat_id}",
                {
                    'type': 'chat_message',
                    'message': 'Nova mensagem recebida!',
                }
            )
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        return JsonResponse({'success': False, 'errors': 'Método de requisição inválido'})

# Função de logout padrão do Django
# Não é necessário o decorador @login_required aqui
def custom_logout(request):
    return auth_views.LogoutView.as_view(
        next_page='projeto:pagina_inicial'  # Redireciona para a página inicial após o logout
    )(request)

def custom_login(request, **kwargs):
    return auth_views.LoginView.as_view(
        template_name='comunicacao/login.html',
        extra_context={
            'key': 'value',
        }
    )(request, **kwargs)

@login_required
def pagina_inicial(request):
    return render(request, 'comunicacao/base.html')

@login_required
def lista_chats(request):
    chats = Chat.objects.filter(membros=request.user)
    return render(request, 'comunicacao/lista_chats.html', {'chats': chats})


@login_required
def visualizar_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, membros=request.user)
    mensagens = chat.mensagens_chat.all()

    if request.method == 'POST':
        form = MensagemForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                mensagem = form.save(commit=False)
                mensagem.remetente = request.user
                mensagem.chat = chat
                mensagem.save()
            return redirect('projeto:visualizar_chat', chat_id=chat_id)
    else:
        form = MensagemForm()

    return render(request, 'comunicacao/visualizar_chat.html', {'chat': chat, 'mensagens': mensagens, 'form': form})
