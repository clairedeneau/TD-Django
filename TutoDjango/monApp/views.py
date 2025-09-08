from django.shortcuts import render
from .models import *

# Create your views here.
from django.http import HttpResponse
def home(request, param = None):
 if param :
    return HttpResponse(f"<h1>Bonjour {param} !</h1>")
 return HttpResponse("<h1>Hello Django!</h1>")

def contact(request):
 return HttpResponse("<h1>Contact us</h1>\n<p> Ou pas</p>")

def about(request):
 return HttpResponse("<h1>About...</h1>")

def liste_produits(request):
    prdts = Produit.objects.all()
    rep = "<ul>"
    for prod in prdts:
        rep += f"<li><h2>{prod.intituleProd}<h2>"
        rep += f"<ul><li>Catégorie: {prod.categorie or "Aucune"}</li></ul></li>"
    rep += "</ul>"
    return HttpResponse(rep)

def liste_categories(request):
    cats = Categorie.objects.all()
    rep = "<ul>"
    for cat in cats:
        rep += f"<li><h2>{cat.nomCat or "Untitled"}<h2>"
        rep += f"<ul><li>Identifiant: {cat.idCat}</li></ul></li>"
    rep += "</ul>"
    return HttpResponse(rep)

def liste_statuts(request):
    stats = Statut.objects.all()
    rep = "<ul>"
    for stat in stats:
        rep += f"<li><h2>{stat.libelle or "Untitled"}<h2>"
        rep += f"<ul><li>Identifiant: {stat.idStatut}</li></ul></li>"
    rep += "</ul>"
    return HttpResponse(rep)