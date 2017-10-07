from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def index(request):
    context_dict = {}
    return render(request, 'index.html', context_dict)
