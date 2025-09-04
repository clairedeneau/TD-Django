from django.shortcuts import render

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