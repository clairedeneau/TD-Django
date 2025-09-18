from django.contrib import admin
from .models import *
from decimal import *

class ProduitAdmin(admin.ModelAdmin):
 list_display = ('intituleProd', 'prixUnitaireProd')

admin.site.register(Produit)
admin.site.register(Categorie)
admin.site.register(Statut)
admin.site.register(Rayon)
admin.site.register(Contenir)
# Register your models here.

class ProduitInline(admin.TabularInline):
    model = Produit
    extra = 1 # nombre de lignes vides par défaut

class CategorieAdmin(admin.ModelAdmin):
    model = Categorie
    inlines = [ProduitInline]

class ProduitFilter(admin.SimpleListFilter):
    title = 'filtre produit'
    parameter_name = 'custom_status'

    def lookups(self, request, model_admin) :
        return (
        ('OnLine', 'En ligne'),
        ('OffLine', 'Hors ligne'),
        )
    def queryset(self, request, queryset):
        if self.value() == 'OnLine':
            return queryset.filter(status=1)
        if self.value() == 'OffLine':
            return queryset.filter(status=0)

def set_Produit_online(modeladmin, request, queryset):
    queryset.update(status=1)
set_Produit_online.short_description = "Mettre en ligne"
def set_Produit_offline(modeladmin, request, queryset):
    queryset.update(status=0)
set_Produit_offline.short_description = "Mettre hors ligne"

class ProduitAdmin(admin.ModelAdmin):
    model = Produit
    list_display = ["refProd", "intituleProd", "prixUnitaireProd","prixTTCProd" "dateFabProd", "categorie", "status"]
    list_editable = ["intituleProd", "prixUnitaireProd"]
    radio_fields = {"status": admin.VERTICAL}
    search_fields = ('intituleProd', 'dateFabProd')
    list_filter = (ProduitFilter,)
    date_hierarchy = 'dateFabProd'
    ordering = ('-dateFabProd',)
    actions = [set_Produit_online, set_Produit_offline]

    def prixTTCProd(self, instance):
        return (instance.prixUnitaireProd * Decimal('1.20')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    prixTTCProd.short_description = "Prix TTC"
    prixTTCProd.admin_order_field = "prixUnitaireProd"