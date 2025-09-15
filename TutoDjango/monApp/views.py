from django.shortcuts import render
from .models import *
from django.http import HttpResponse, Http404

# Create your views here.

def home(request, param):
    if request.GET and request.GET["test"]:
        raise Http404
    return HttpResponse("<h1>Hello " + param + " ! You're connected</h1>")

def contact(request):
    return render(request, 'monApp/contact.html')

def about(request):
    return render(request, 'monApp/about.html')

def liste_produits(request):
    prdts = Produit.objects.all()
    return render(request, 'monApp/list_produits.html', {'prdts': prdts})

def liste_categories(request):
    cats = Categorie.objects.all()
    return render(request, 'monApp/list_categories.html', {'cats': cats})

def liste_statuts(request):
    stats = Statut.objects.all()
    return render(request, 'monApp/list_statuts.html', {'stats': stats})

def liste_rayons(request):
    rays = Rayon.objects.all()
    return render(request, 'monApp/list_rayons.html', {'rays': rays})