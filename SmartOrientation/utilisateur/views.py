from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages


def accueil(request):
    return render(request, 'accueil.html')


def inscription(request):
    if request.method == 'POST':

        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        motdepasse = request.POST.get('motdepasse')
        confirmation = request.POST.get('confirmation')

        # Vérifier les mots de passe
        if motdepasse != confirmation:
            messages.error(
                request,
                "Les mots de passe ne correspondent pas."
            )
            return redirect('inscription')

        # Vérifier si l'e-mail existe déjà
        if User.objects.filter(email=email).exists():
            messages.error(
                request,
                "Cette adresse e-mail est déjà utilisée."
            )
            return redirect('inscription')

        # Créer le compte
        User.objects.create_user(
            username=email,
            email=email,
            password=motdepasse,
            first_name=prenom,
            last_name=nom
        )

        # Message de succès
        messages.success(
            request,
            "Compte créé avec succès ! Vous pouvez maintenant vous connecter."
        )

        # Aller vers la page de connexion
        return redirect('connexion')

    return render(request, 'inscription.html')


def connexion(request):
    if request.method == 'POST':

        email = request.POST.get('email')
        motdepasse = request.POST.get('motdepasse')

        # Vérifier les identifiants
        user = authenticate(
            request,
            username=email,
            password=motdepasse
        )

        if user is not None:
            # Connecter l'utilisateur
            login(request, user)

            # Aller vers l'analyse d'orientation
            return redirect('orientation_analyse')

        # Identifiants incorrects
        messages.error(
            request,
            "Adresse e-mail ou mot de passe incorrect."
        )

    return render(request, 'connexion.html') 