from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator, RegexValidator

PasswordValidator = RegexValidator(r'[\w ._,!\/$\-@#%\^&*+?]+')

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Email', 'autofocus':'1'}),
                            max_length=150, validators=[EmailValidator], label="Email")

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                               max_length=150, validators=[PasswordValidator], label="Password")

    class Meta:
        fields = ('email', 'password')


class RegistrationForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Name', 'autofocus':'1'}),
        max_length=150, validators=[UnicodeUsernameValidator], label="Name")

    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Email address'}),
                            max_length=150, validators=[EmailValidator], label="Email")

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}),
                               max_length=150, min_length=10, validators=[PasswordValidator], label="Password")

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Confirm password'}), max_length=150,
        validators=[PasswordValidator], label="Confirm Password")

    class Meta:
        fields = ('name', 'email', 'password')

class UpdateForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Name', 'autofocus':'1'}),
        max_length=150, validators=[UnicodeUsernameValidator], label="Name")

    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Email address'}),
                            max_length=150, validators=[EmailValidator], label="Email")

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}),
                               max_length=150, min_length=10, validators=[PasswordValidator], label="Password")

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Confirm password'}), max_length=150,
        validators=[PasswordValidator], label="Confirm Password")

    class Meta:
        fields = ('name', 'email', 'password')
