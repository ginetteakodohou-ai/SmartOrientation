import json
from django.shortcuts import render
from .models import Baccalaureat, Filiere

def orientation_view(request):
    donnees_matieres = {}
    donnees_filieres = {}

    bacs = Baccalaureat.objects.all()

    for bac in bacs:
        donnees_matieres[bac.nom] = []
        donnees_filieres[bac.nom] = []

        coefficients = bac.coefficients.select_related("matiere")

        for coef in coefficients:
            donnees_matieres[bac.nom].append({
                "id": coef.matiere.id,
                "nom": coef.matiere.nom,
                "code": f"note_{coef.matiere.id}",
                "coefficient": coef.coefficient,
            })

        filieres = Filiere.objects.filter(
            bac=bac
        ).select_related(
            "etablissement",
            "etablissement__Universite"
        )

        for filiere in filieres:
            donnees_filieres[bac.nom].append({
                "id": filiere.id,
                "nom": filiere.nom,
                "niveau": filiere.niveau,
                "etablissement": filiere.etablissement.nom,
                "universite": filiere.etablissement.Universite.nom,
                "bourse": filiere.bourse,
                "secour": filiere.secour,
                "deboucher": filiere.deboucher,
            })

    context = {
    "donnees_matieres_json": donnees_matieres,
    "donnees_filieres_json": donnees_filieres,}

    return render(request, "orientations/orientation.html", context)

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Baccalaureat

@require_POST
def analyser_profil(request):

    data = json.loads(request.body)

    serie = data.get('serie')
    notes = data.get('notes', {})
    interets = data.get('interets', [])
    moyenne_ponderee = float(data.get('moyenne_ponderee', 0))

    try:
        bac = Baccalaureat.objects.get(nom=serie)
    except Baccalaureat.DoesNotExist:
        return JsonResponse({'erreur': 'Série invalide'}, status=400)

    # Placeholder en attendant le vrai scoring des filières
    resultats = []

    return JsonResponse({'filieres': resultats})

from .calcul import calculer_scores_filieres

@require_POST
def analyser_profil(request):

    data = json.loads(request.body)

    serie = data.get('serie')
    notes = data.get('notes', {})
    interets = data.get('interets', [])

    try:
        bac = Baccalaureat.objects.get(nom=serie)
    except Baccalaureat.DoesNotExist:
        return JsonResponse({'erreur': 'Série invalide'}, status=400)

    resultats = calculer_scores_filieres(bac, notes, interets)

    return JsonResponse({'filieres': resultats})