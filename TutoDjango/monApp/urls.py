from django.urls import path
from . import views
urlpatterns = [
 path("home/<param>", views.home, name="home"),
 path("home/", views.home, name="home"),
 path("contact/", views.contact, name="contact"),
 path("about/", views.about, name="about"),
 path("listeprods/", views.liste_produits, name="prod_list"),
 path("listecats/", views.liste_categories, name="cat_list"),
 path("listestats/", views.liste_statuts, name="stat_list"),
 path("listerays/", views.liste_rayons, name="ray_list"),
]