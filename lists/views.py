from django.shortcuts import render
from django.http import HttpResponse
home_page = None
# Create your views here.
def home_page(request):
    return render(request, 'home.html')