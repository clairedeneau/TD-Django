from django.shortcuts import render
from .models import *
from django.http import HttpResponse, Http404
from django.views.generic import *

# Create your views here.

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

class HomeView(TemplateView):
    template_name = "monApp/page_home.html"
    def post(self, request, **kwargs):
        return render(request, self.template_name)
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['titreh1'] = f"Hello {self.kwargs.get('param') or "Django"} !"
        return context
    
class AboutView(TemplateView):
    template_name = "monApp/page_home.html"
    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['titreh1'] = "About us... nothing"
        return context
    
    def post(self, request, **kwargs):
        return render(request, self.template_name)
    
class ContactView(TemplateView):
    template_name = "monApp/page_home.html"
    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['titreh1'] = "DO NOT CONTACT ME"
        return context
    
    def post(self, request, **kwargs):
        return render(request, self.template_name)
    
class ProduitListView(ListView):
    model = Produit
    template_name = "monApp/list_produits.html"
    context_object_name = "prdts"

    def get_queryset(self ) :
        return Produit.objects.order_by("prixUnitaireProd")
    
    def get_context_data(self, **kwargs):
        context = super(ProduitListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes produits"
        return context
    
class ProduitDetailView(DetailView):
    model = Produit
    template_name = "monApp/detail_produit.html"
    context_object_name = "prdt"

    def get_context_data(self, **kwargs):
        context = super(ProduitDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du produit"
        return context
    
