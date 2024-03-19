from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'projeto'

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('lista_chats/', views.lista_chats, name='lista_chats'),
    path('visualizar_chat/<int:chat_id>/', views.visualizar_chat, name='visualizar_chat'),
    path('enviar_mensagem/<int:chat_id>/', views.enviar_mensagem, name='enviar_mensagem'),
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
