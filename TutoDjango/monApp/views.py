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
from django.db.models import Count, Prefetch
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

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

    def get_queryset(self):
    # Surcouche pour filtrer les résultats en fonction de la recherche
    # Récupérer le terme de recherche depuis la requête GET
        query = self.request.GET.get('search')
        if query:
            return Produit.objects.filter(intituleProd__icontains=query).select_related('categorie').select_related('status')

        # Si aucun terme de recherche, retourner tous les produits
        # Charge les catégories en même temps
        return Produit.objects.select_related('categorie').select_related('status')
    
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

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            return Categorie.objects.filter(nomCat__icontains=query).annotate(nb_produits=Count('produits_categorie'))
        return Categorie.objects.annotate(nb_produits=Count('produits_categorie'))
    
    def get_context_data(self, **kwargs):
        context = super(CatListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des catégories"
        return context
    
class CatDetailView(DetailView):
    model = Categorie
    template_name = "monApp/detail_categorie.html"
    context_object_name = "cat"

    def get_queryset(self):
        return Categorie.objects.annotate(nb_produits=Count('produits_categorie'))

    def get_context_data(self, **kwargs):
        context = super(CatDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail de la catégorie"
        context['prdts'] = self.object.produits_categorie.all()
        return context
    
class StatutListView(ListView):
    model = Statut
    template_name = "monApp/list_statuts.html"
    context_object_name = "stats"

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            return Statut.objects.filter(libelleStatus__icontains=query).annotate(nb_produits=Count('produits_status'))
        return Statut.objects.annotate(nb_produits=Count('produits_status'))
    
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
    
    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            Rayon.objects.filter(nomRayon__icontains=query).prefetch_related(Prefetch("contenir_rayon", queryset=Contenir.objects.select_related("produit")))
        return Rayon.objects.prefetch_related(Prefetch("contenir_rayon", queryset=Contenir.objects.select_related("produit")))
    
    def get_context_data(self, **kwargs):
        context = super(RayonListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes rayons"
        ryns_dt = []
        for rayon in context['rays']:
            total = 0
            for contenir in rayon.contenir_rayon.all():
                total += contenir.produit.prixUnitaireProd * contenir.Qte
            ryns_dt.append({'rayon': rayon,'total_stock': total})
        context['ryns_dt'] = ryns_dt
        return context
    
class RayonDetailView(DetailView):
    model = Rayon
    template_name = "monApp/detail_rayon.html"
    context_object_name = "rayon"

    def get_context_data(self, **kwargs):
        context = super(RayonDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du rayon"

        prdts_dt = []
        total_rayon = 0
        total_nb_produit = 0
        for contenir in self.object.contenir_rayon.all():
            total_produit = contenir.produit.prixUnitaireProd * contenir.Qte
            prdts_dt.append({ 'produit': contenir.produit,
                            'qte': contenir.Qte,
                            'prix_unitaire': contenir.produit.prixUnitaireProd,
                            'total_produit': total_produit} )
            total_rayon += total_produit
            total_nb_produit += contenir.Qte
        context['prdts_dt'] = prdts_dt
        context['total_rayon'] = total_rayon
        context['total_nb_produit'] = total_nb_produit

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

@method_decorator(login_required, name='dispatch')
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
    
@method_decorator(login_required, name='dispatch')
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
    
@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView):
    model = Produit
    template_name = "monApp/delete.html"
    success_url = reverse_lazy('lst_prdts')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Supprimer un produit"
        context["texte"] = f"Êtes-vous sûr de vouloir supprimer le produit '{context['object'].intituleProd}' ?"
        return context
    
@method_decorator(login_required, name='dispatch')
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
    
@method_decorator(login_required, name='dispatch')
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
    
@method_decorator(login_required, name='dispatch')
class StatutDeleteView(DeleteView):
    model = Statut
    template_name = "monApp/delete.html"
    success_url = reverse_lazy('stat_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Supprimer un statut"
        context["texte"] = f"Êtes-vous sûr de vouloir supprimer le statut '{context['object'].libelleStatus}' ?"
        return context
    
@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
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
    
@method_decorator(login_required, name='dispatch')
class CategorieDeleteView(DeleteView):
    model = Categorie
    template_name = "monApp/delete.html"
    success_url = reverse_lazy('cat_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Supprimer une catégorie"
        context["texte"] = f"Êtes-vous sûr de vouloir supprimer la catégorie '{context['object'].nomCat}' ?"
        return context
    
@method_decorator(login_required, name='dispatch')
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
    
@method_decorator(login_required, name='dispatch')
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
    
@method_decorator(login_required, name='dispatch')
class RayonDeleteView(DeleteView):
    model = Rayon
    template_name = "monApp/delete.html"
    success_url = reverse_lazy('ray_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Supprimer un rayon"
        context["texte"] = f"Êtes-vous sûr de vouloir supprimer le rayon '{context['object'].nomRayon}' ?"
        return context
    
@method_decorator(login_required, name='dispatch')
class ContenirCreateView(CreateView):
    model = Contenir
    form_class = ContenirForm
    template_name = "monApp/create.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        contenir = form.save(commit=False)
        contenir.rayon_id = self.kwargs['pk']

        existing = Contenir.objects.filter(
            rayon_id=contenir.rayon_id,
            produit=contenir.produit
        ).first()

        if existing:
            existing.Qte = contenir.Qte
            existing.save()
            return redirect('dtl_rayon', existing.rayon.idRayon)

        contenir.save()
        return redirect('dtl_rayon', contenir.rayon.idRayon)

    def get_initial(self):
        return {'rayon': Rayon.objects.get(pk=self.kwargs['pk'])}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Ajouter un produit au rayon"
        return context
    
@method_decorator(login_required, name='dispatch')
class ContenirUpdateView(UpdateView):
    model = Contenir
    form_class = ContenirForm
    template_name = "monApp/update.html"
    def get_object(self):
        return Contenir.objects.get(rayon_id=self.kwargs['pk'], produit_id=self.kwargs['produit_id'])
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        contenir = form.save()
        return redirect('dtl_rayon', contenir.rayon.idRayon)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Mettre à jour la quantité"
        return context
    
@method_decorator(login_required, name='dispatch')
class ContenirDeleteView(DeleteView):
    model = Contenir
    template_name = "monApp/delete.html"

    def get_object(self):
        return Contenir.objects.get(rayon_id=self.kwargs['pk'], produit_id=self.kwargs['produit_id'])

    def get_success_url(self):
        return reverse_lazy('dtl_rayon', kwargs={'pk': self.object.rayon.idRayon})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Supprimer un produit du rayon"
        context["texte"] = f"Êtes-vous sûr de vouloir supprimer le produit '{context['object'].produit.intituleProd}' du rayon '{context['object'].rayon.nomRayon}' ?"
        return context