from django.shortcuts import render

# Create your views here.

def inscription(request):
   return render(request, 'inscription.html')

def accueil(request):
    return render(request, 'accueil.html')

    
def connexion(request):
    return render(request, 'connexion.html')


