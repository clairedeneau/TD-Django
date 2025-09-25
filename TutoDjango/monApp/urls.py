from django.urls import path
from . import views
from django.views.generic import *

urlpatterns = [
 #path("home/<param>", views.home, name="home"),
 #path("home/", views.home, name="home"),
 #path("contact/", views.contact, name="contact"),
 #path("about/", views.about, name="about"),
 path("listeprods/", views.ProduitListView.as_view(), name="lst_prdts"),
 path("listecats/", views.CatListView.as_view(), name="cat_list"),
 path("listestats/", views.StatutListView.as_view(), name="stat_list"),
 path("listerays/", views.RayonListView.as_view(), name="ray_list"),
 path("home/", views.HomeView.as_view()),
 path("home/<param>", views.HomeView.as_view()),
 path("about/", views.AboutView.as_view()),
 path("contact/", views.ContactView.as_view()),
 path("produit/<pk>/",views.ProduitDetailView.as_view(), name="dtl_prdt"),
 path("categorie/<pk>/",views.CatDetailView.as_view(), name="dtl_cat"),
 path("statut/<pk>/",views.StatutDetailView.as_view(), name="dtl_stat"),
 path("rayon/<pk>/",views.RayonDetailView.as_view(), name="dtl_ray"),
 path('login/', views.ConnectView.as_view(), name='login'),
path('register/', views.RegisterView.as_view(), name='register'),
path('logout/', views.DisconnectView.as_view(), name='logout'),
]
