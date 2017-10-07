from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from registration.forms import RegistrationForm, LoginForm, UpdateForm
from django.contrib.auth.models import User

from ethefux_app.models import UserProfile

def user_register(request):
    registered = False
    user_form = RegistrationForm()

    # If we are getting a new user
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)

        # Make sure the new user has put in all the right details
        if user_form.is_valid():
            name = user_form.cleaned_data.get("name")
            email = user_form.cleaned_data.get("email")
            password = user_form.cleaned_data.get("password")
            password_confirm = user_form.cleaned_data.get("password_confirm")
            home_address = user_form.cleaned_data.get("home_address")

            
            registered = True

            if password == password_confirm:
                if email is not "":
                    new_user, created = User.objects.get_or_create(username=email)

                    # Make sure the new user isnt recreating an account that already exists
                    if created:
                        new_user.email = email
                        new_user.set_password(password)
                        new_user.save()

                        profile = UserProfile.objects.create(user=new_user)
                        profile.name = name
                        profile.save()

                        return HttpResponseRedirect(reverse("registration:user_login"))
                    else:
                        user_form.add_error("email", 'That user already exists! Are you sure you don\'t already have an account?')
                else:
                    user_form.add_error('email', 'Please enter a valid email!')
            else:
                user_form.add_error('password_confirm', 'Passwords do not match!')

    return render(request, "registration/register.html", {"form": user_form})


def user_login(request):
    user_form = LoginForm()
    context_dict = {}

    if request.method == "POST":
        user_form = LoginForm(request.POST)

        if user_form.is_valid():
            user = authenticate(username=user_form.cleaned_data.get("email"),
                                password=user_form.cleaned_data.get("password"))

            if (user):
                login(request, user)
                return HttpResponseRedirect(reverse("ethefux_app:dashboard"))
            else:
                user_form.add_error(None, "Incorrect email or password!")

    context_dict["form"] = user_form
    return render(request, "registration/login.html", context_dict)

@login_required
def user_update(request):
    user_form = UpdateForm()

    # If we are getting a new user
    if request.method == "POST":
        user_form = UpdateForm(request.POST)

        # Make sure the new user has put in all the right details
        if user_form.is_valid():
            name = user_form.cleaned_data.get("name")
            email = user_form.cleaned_data.get("email")
            password = user_form.cleaned_data.get("password")
            password_confirm = user_form.cleaned_data.get("password_confirm")

            if password == password_confirm:
                if email is not "":
                    new_user, created = User.objects.get_or_create(username=email)

                    # Make sure the new user isnt recreating an account that already exists
                    if (created):
                        new_user.email = email
                        new_user.set_password(password)
                        new_user.save()

                        profile = UserProfile.objects.create(user=new_user)
                        profile.name = name
                        profile.save()

                        return HttpResponseRedirect(reverse("registration:user_login"))
                    else:
                        user_form.add_error("email", 'That user already exists! Are you sure you don\'t already have an account?')
                else:
                    user_form.add_error('email', 'Please enter a valid email!')
            else:
                user_form.add_error('password_confirm', 'Passwords do not match!')

    return render(request, "registration/update.html", {"form": user_form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
