from django.shortcuts import render
from django.http import HttpResponse
home_page = None
from lists.models import Item, List
from django.shortcuts import redirect
# Create your views here.
def home_page(request):
    return render(request,'home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items':items})

def new_list(request):
    list_user = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_user)
    return redirect('/lists/the-new-page/')