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