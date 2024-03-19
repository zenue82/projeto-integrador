from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)  

    def __str__(self):
        return self.user.username


class Chat(models.Model):
    membros = models.ManyToManyField(User)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.pk}"

class Mensagem(models.Model):
    chat = models.ForeignKey(Chat, related_name='mensagens_chat', on_delete=models.CASCADE)
    remetente = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensagem de {self.remetente} em {self.chat} em {self.data_envio}"


class Forum(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()

class Topico(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    corpo = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)

class MensagemTopico(models.Model):
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE)
    corpo = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    data_envio = models.DateTimeField(auto_now_add=True)

class Lembrete(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    data_lembrete = models.DateTimeField()

class Feedback(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    corpo = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
