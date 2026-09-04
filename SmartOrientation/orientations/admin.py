from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Universite)
admin.site.register(models.Etablissement)
admin.site.register(models.Matiere)
admin.site.register(models.Baccalaureat)

@admin.register(models.Filiere)
class UniversiteAdmin(admin.ModelAdmin):
    list_display = ['nom','etablissement']

admin.site.register(models.Coefficient)

admin.site.register(models.CentreInteret)