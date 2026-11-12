from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from .models import Service


def catalog(request):
    services = Service.objects.all()
    return render(request, 'catalog.html', {'services': services})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('catalog')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! Регистрация прошла успешно.')
            return redirect('catalog')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('catalog')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'С возвращением, {user.username}!')
                return redirect('catalog')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('catalog')