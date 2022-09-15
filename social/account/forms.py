from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
from post.forms import PostForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=25,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    # profile_link = forms.SlugField(widget=forms.SlugField(attrs={'class': 'form-control', 'autocomplete': 'off'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileEditForm(forms.ModelForm):


    class Meta:
        model = Profile
        
        fields = ('bio', 'profile_pic', )
