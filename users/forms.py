from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

from django import forms
from django.contrib.auth.forms import UserCreationForm
from AppFixB1.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=255, required=False, label= 'Name: *(Unrequired)')
    surname = forms.CharField(max_length=255, required=False, label = 'Surname: *(Unrequired)')


    class Meta:
        model = User

        fields = ('login', 'email', 'password1', 'password2', 'name', 'surname' )




