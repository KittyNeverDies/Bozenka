from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import LoginForm, RegisterForm


def auth_view(request):
    login_form = LoginForm()
    register_form = RegisterForm()

    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    messages.success(request, f'Hi {username.title()}, welcome back!')
                    return redirect('home')
                else:
                    messages.error(request, f'Invalid username or password')
        elif 'register' in request.POST:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                messages.success(request, 'You have signed up successfully.')
                login(request, user)
                return redirect('home')

    return render(request, 'accounts/index.html', {
        'login_form': login_form,
        'register_form': register_form
    })