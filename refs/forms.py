from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *

class AddWorkForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['cat'].empty_label='Категория не выбрана'

    class Meta:
        model=Reflist
        fields=['title','file','cat']
        widjets={
            'title':forms.TextInput(attrs={'class':'form-input'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 1000:
            raise ValidationError('Длина превышает 10 символов')

        return title

class RegisterUserForm(UserCreationForm):
    username=forms.CharField(label='Логин',widget=forms.TextInput(attrs={'class':'form-input'}))
    email=forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class':'form-input'}))
    password1 =forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class':'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model=User
        fields=('username','email','password1','password2')

class LoginUserForm(AuthenticationForm):
    username=forms.CharField(label='Логин',widget=forms.TextInput(attrs={'class':'form-input'}))
    password =forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class':'form-input'}))

class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields=['name','email','content']
        widjets={
            'title':forms.TextInput(attrs={'class':'form-input'}),
        }
    
class SearchForm(forms.Form):
    title=forms.CharField(label='Введите заголовок', max_length=255)

