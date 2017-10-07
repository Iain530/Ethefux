from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator, RegexValidator

PasswordValidator = RegexValidator(r'[\w ._,!\/$\-@#%\^&*+?]+')

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                            max_length=150, validators=[EmailValidator], label="")

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               max_length=150, validators=[PasswordValidator], label="")

    class Meta:
        fields = ('email', 'password')


class RegistrationForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=150, validators=[UnicodeUsernameValidator])

    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}),
                            max_length=150, validators=[EmailValidator])

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               max_length=150, min_length=10, validators=[PasswordValidator])

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), max_length=150,
        validators=[PasswordValidator], label="Confirm Password")

    class Meta:
        fields = ('name', 'email', 'password')


