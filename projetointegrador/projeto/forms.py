from django import forms
from .models import Mensagem
from django.contrib.auth.models import User
from .models import Profile

class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ['texto']


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio',)
