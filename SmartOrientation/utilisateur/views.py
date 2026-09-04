from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

# 1. Page d'accueil
def accueil(request):
    return render(request, 'accueil.html')

# 2. Page d'inscription
def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Enregistre le nouvel utilisateur en BDD
            login(request, user)  # Connecte l'utilisateur immédiatement
            messages.success(request, "Inscription réussie !")
            return redirect('orientation_analyse')  # Redirige directement vers l'orientation
    else:
        form = UserCreationForm()
    return render(request, 'inscription.html', {'form': form})

# 3. Page de connexion
def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Crée la session utilisateur
            return redirect('orientation_analyse')  # Redirige vers la page d'orientation
    else:
        form = AuthenticationForm()
    return render(request, 'connexion.html', {'form': form})
