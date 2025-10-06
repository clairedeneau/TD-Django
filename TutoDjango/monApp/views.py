from django.forms import BaseModelForm
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.generic import  *
from monApp.forms import *
from monApp.models import *
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse_lazy

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
    template_name = "monApp/about.html"
    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['titreh1'] = "About us... nothing"
        return context
    
    def post(self, request, **kwargs):
        return render(request, self.template_name)
    
class ConfirmView(TemplateView):
    template_name = "monApp/confirm.html"
    def get_context_data(self, **kwargs):
        context = super(ConfirmView, self).get_context_data(**kwargs)
        context['titreh1'] = "Email envoyé"
        return context
    
    def post(self, request, **kwargs):
        return render(request, self.template_name)
    
def ContactView(request):
    titreh1 = "Contact us !"
    if request.method=='POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            send_mail(
            subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via TutoDjango Contact form',
            message=form.cleaned_data['message'],
            from_email=form.cleaned_data['email'],
            recipient_list=['admin@monApp.com'],
            )
            return redirect('confirm')
    else:
        form = ContactUsForm()
    return render(request, "monApp/page_home.html",{'titreh1':titreh1, 'form':form})
    
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
    
class CatListView(ListView):
    model = Categorie
    template_name = "monApp/list_categories.html"
    context_object_name = "cats"

    def get_queryset(self) :
        return Categorie.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(CatListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des catégories"
        return context
    
class CatDetailView(DetailView):
    model = Categorie
    template_name = "monApp/detail_categorie.html"
    context_object_name = "cat"

    def get_context_data(self, **kwargs):
        context = super(CatDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail de la catégorie"
        return context
    
class StatutListView(ListView):
    model = Statut
    template_name = "monApp/list_statuts.html"
    context_object_name = "stats"

    def get_queryset(self) :
        return Statut.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(StatutListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des statuts"
        return context
    
class StatutDetailView(DetailView):
    model = Statut
    template_name = "monApp/detail_statut.html"
    context_object_name = "stat"

    def get_context_data(self, **kwargs):
        context = super(StatutDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du statut"
        return context
    
class RayonListView(ListView):
    model = Rayon
    template_name = "monApp/list_rayons.html"
    context_object_name = "rays"

    def get_queryset(self) :
        return Rayon.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(RayonListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des rayons"
        return context
    
class RayonDetailView(DetailView):
    model = Rayon
    template_name = "monApp/detail_rayon.html"
    context_object_name = "ray"

    def get_context_data(self, **kwargs):
        context = super(RayonDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du rayon"
        return context
    
class ConnectView(LoginView):
    template_name = 'monApp/page_login.html'
    def post(self, request, **kwargs):
        lgn = request.POST.get('username', False)
        pswrd = request.POST.get('password', False)
        user = authenticate(username=lgn, password=pswrd)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'monApp/page_home.html', {'param': lgn, 'message': "You're connected"})
        else:
            return render(request, 'monApp/page_register.html')
        
class RegisterView(TemplateView):
    template_name = 'monApp/page_register.html'
    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        mail = request.POST.get('mail', False)
        password = request.POST.get('password', False)
        user = User.objects.create_user(username, mail, password)
        user.save()
        if user is not None and user.is_active:
            return render(request, 'monApp/page_login.html')
        else:
            return render(request, 'monApp/page_register.html')
        
class DisconnectView(TemplateView):
    template_name = 'monApp/page_logout.html'
    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name)
    
class ProduitCreateView(CreateView):
    model = Produit
    form_class=ProduitForm
    template_name = "monApp/create.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        prdt = form.save()
        return redirect('dtl_prdt', prdt.refProd)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Créer un nouveau produit"
        return context
    
class ProduitUpdateView(UpdateView):
    model = Produit
    form_class=ProduitForm
    template_name = "monApp/update.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        prdt = form.save()
        return redirect('dtl_prdt', prdt.refProd)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Mettre à jour un produit"
        return context
    
class ProductDeleteView(DeleteView):
    model = Produit
    template_name = "monApp/delete.html"
    success_url = reverse_lazy('lst_prdts')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Supprimer un produit"
        context["texte"] = f"Êtes-vous sûr de vouloir supprimer le produit '{context['object'].intituleProd}' ?"
        return context
    
class StatutCreateView(CreateView):
    model = Statut
    form_class = StatutForm
    template_name = "monApp/create.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        stat = form.save()
        return redirect('dtl_stat', stat.idStatus)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Créer un nouveau statut"
        return context
    
class StatutUpdateView(UpdateView):
    model = Statut
    form_class = StatutForm
    template_name = "monApp/update.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        stat = form.save()
        return redirect('dtl_stat', stat.idStatus)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Mettre à jour un statut"
        return context
    
class StatutDeleteView(DeleteView):
    model = Statut
    template_name = "monApp/delete.html"
    success_url = reverse_lazy('stat_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Supprimer un statut"
        context["texte"] = f"Êtes-vous sûr de vouloir supprimer le statut '{context['object'].libelleStatus}' ?"
        return context
    
class CategorieCreateView(CreateView):
    model = Categorie
    form_class = CategorieForm
    template_name = "monApp/create.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        cat = form.save()
        return redirect('dtl_cat', cat.idCat)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Créer une nouvelle catégorie"
        return context
    
class CategorieUpdateView(UpdateView):
    model = Categorie
    form_class = CategorieForm
    template_name = "monApp/update.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        cat = form.save()
        return redirect('dtl_cat', cat.idCat)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Mettre à jour une catégorie"
        return context
    
class CategorieDeleteView(DeleteView):
    model = Categorie
    template_name = "monApp/delete.html"
    success_url = reverse_lazy('cat_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Supprimer une catégorie"
        context["texte"] = f"Êtes-vous sûr de vouloir supprimer la catégorie '{context['object'].nomCat}' ?"
        return context
    
class RayonCreateView(CreateView):
    model = Rayon
    form_class = RayonForm
    template_name = "monApp/create.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        rayon = form.save()
        return redirect('dtl_ray', rayon.idRayon)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Créer un nouveau rayon"
        return context
    
class RayonUpdateView(UpdateView):
    model = Rayon
    form_class = RayonForm
    template_name = "monApp/update.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        rayon = form.save()
        return redirect('dtl_ray', rayon.idRayon)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Mettre à jour un rayon"
        return context
    
class RayonDeleteView(DeleteView):
    model = Rayon
    template_name = "monApp/delete.html"
    success_url = reverse_lazy('ray_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Supprimer un rayon"
        context["texte"] = f"Êtes-vous sûr de vouloir supprimer le rayon '{context['object'].nomRayon}' ?"
        return context