from django.db import models

# Create your models here.

class Universite(models.Model):
    nom = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.nom

class Etablissement(models.Model):

    nom = models.CharField(max_length=300)
    Universite = models.ForeignKey(Universite,on_delete=models.CASCADE,related_name="etablissements")

    def __str__(self):
        return self.nom



class Matiere(models.Model):
    nom = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.nom

class Baccalaureat(models.Model):
    nom = models.CharField(max_length=10,unique=True)

    def __str__(self):
        return self.nom

class CentreInteret(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

class Filiere(models.Model):
    nom = models.CharField(max_length=200)
    etablissement = models.ForeignKey(Etablissement,on_delete=models.CASCADE,related_name="filieres")
    MODE = [('Classement','Classement'), 
                ('Concours','Concours')]
    niveau = models.CharField(max_length=50, choices=MODE)
    matiere = models.ManyToManyField(Matiere,related_name="matiere")

    bac = models.ManyToManyField(Baccalaureat,related_name="bac")

    bourse = models.PositiveIntegerField()
    secour = models.PositiveIntegerField()

    deboucher = models.TextField()

    centre_interet = models.ForeignKey(CentreInteret,on_delete=models.CASCADE,null=True,blank=True,related_name="filieres")

    def __str__(self):
        return self.nom

class Coefficient(models.Model):
    matiere = models.ForeignKey(
        Matiere,
        on_delete=models.CASCADE,
        related_name="coefficients"
    )

    bac = models.ForeignKey(
        Baccalaureat,
        on_delete=models.CASCADE,
        related_name="coefficients"
    )

    coefficient = models.FloatField()

    class Meta:
        unique_together = ("matiere", "bac")

    def __str__(self):
        return f"{self.matiere} - BAC {self.bac} : {self.coefficient}"
