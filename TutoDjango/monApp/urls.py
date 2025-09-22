from django.urls import path
from . import views
from django.views.generic import *

urlpatterns = [
 #path("home/<param>", views.home, name="home"),
 #path("home/", views.home, name="home"),
 #path("contact/", views.contact, name="contact"),
 #path("about/", views.about, name="about"),
 path("listeprods/", views.ProduitListView.as_view(), name="lst_prdts"),
 path("listecats/", views.liste_categories, name="cat_list"),
 path("listestats/", views.liste_statuts, name="stat_list"),
 path("listerays/", views.liste_rayons, name="ray_list"),
 path("home/", views.HomeView.as_view()),
 path("home/<param>", views.HomeView.as_view()),
 path("about/", views.AboutView.as_view()),
 path("contact/", views.ContactView.as_view()),
 path("produit/<pk>/",views.ProduitDetailView.as_view(), name="dtl_prdt"),
]