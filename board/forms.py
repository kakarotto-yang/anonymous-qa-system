from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from board.models import *


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'password']

class QuestionForm(forms.ModelForm):
    question = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Ask me any questions.', 'rows': '5', 'cols': '10', 'name': 'question'}),
        required=True,
    )

    question_key = forms.CharField(widget=forms.TextInput(
        attrs={'name': 'question_key'}),
    )

    class Meta:
        model = Question
        fields = ('question', 'question_key')
