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

                        profile = new_user.user_profile
                        profile.name = name
                        profile.home_address = home_address
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
    user = request.user
    user_profile = request.user.user_profile
    user_form = UpdateForm(initial={'name':user_profile.name, 'email':user.email, 'home_address': user_profile.home_address,
                                    'identification': user_profile.identification})

    # If we are getting a new user
    if request.method == "POST":
        user_form = UpdateForm(request.POST, request.FILES)

        # Make sure the new user has put in all the right details
        if user_form.is_valid():
            name = user_form.cleaned_data.get("name")
            email = user_form.cleaned_data.get("email")
            home_address = user_form.cleaned_data.get("home_address")
            password = user_form.cleaned_data.get("password")
            new_password = user_form.cleaned_data.get("new_password")
            new_password_confirm = user_form.cleaned_data.get("new_password_confirm")

            if email is not "":
                if new_password == new_password_confirm:
                    if authenticate(username=request.user.email, password=user_form.cleaned_data.get("password")):

                        request.user.email = email
                        request.user.username = email
                        if new_password:
                            request.user.set_password(new_password)
                        request.user.save()

                        profile = UserProfile.objects.get(user=request.user)

                        if 'identification' in request.FILES:
                            profile.identification = request.FILES['identification']
                        profile.name = name
                        profile.save()

                        login(request, request.user)

                        return HttpResponseRedirect(reverse("ethefux_app:account"))
                    else:
                        user_form.add_error('password', 'Incorrect password!')
                else:
                    user_form.add_error('new_password', 'Passwords do not match!')
            else:
                user_form.add_error('email', 'Please enter a valid email!')
    return render(request, "registration/update.html", {"form": user_form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("ethefux_app:index"))
