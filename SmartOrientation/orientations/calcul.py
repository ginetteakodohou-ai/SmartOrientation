from .models import Filiere, Coefficient

BONUS_CENTRE_INTERET = 2  # points bonus sur 20 si l'intérêt correspond


def calculer_scores_filieres(bac, notes, interets, limite=5):
    """
    bac : instance Baccalaureat
    notes : dict { "note_<matiere_id>": note_float }
    interets : liste de noms de CentreInteret cochés, ex ["informatique", "mathematiques"]
    """

    filieres = Filiere.objects.filter(bac=bac).select_related(
        'etablissement', 'etablissement__Universite', 'centre_interet'
    ).prefetch_related('matiere')

    resultats = []

    for filiere in filieres:

        somme_points = 0
        somme_coefs = 0

        for matiere in filiere.matiere.all():

            code = f"note_{matiere.id}"
            note = notes.get(code)

            if note is None:
                # L'utilisateur n'a pas cette matière (pas dans sa série) → on l'ignore
                continue

            try:
                coefficient = Coefficient.objects.get(
                    matiere=matiere, bac=bac
                ).coefficient
            except Coefficient.DoesNotExist:
                coefficient = 1  # valeur de secours si le coefficient n'est pas défini

            somme_points += note * coefficient
            somme_coefs += coefficient

        if somme_coefs == 0:
            # Aucune matière de cette filière ne correspond à la série de l'utilisateur
            continue

        score_sur_20 = somme_points / somme_coefs

        # Bonus si le centre d'intérêt de la filière est coché par l'utilisateur
        bonus = 0
        if filiere.centre_interet and filiere.centre_interet.nom in interets:
            bonus = BONUS_CENTRE_INTERET

        score_final = min(score_sur_20 + bonus, 20)

        resultats.append({
            'id': filiere.id,
            'nom': filiere.nom,
            'etablissement': filiere.etablissement.nom,
            'universite': filiere.etablissement.Universite.nom,
            'niveau': filiere.niveau,
            'score': round(score_final / 20 * 100, 1),  # en %, pour tes barres de progression
            'bourse': filiere.bourse,
            'secour': filiere.secour,
            'deboucher': filiere.deboucher,
        })

    resultats.sort(key=lambda r: r['score'], reverse=True)

    return resultats[:limite]