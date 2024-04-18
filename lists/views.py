from django.shortcuts import render
from django.http import HttpResponse
home_page = None
from lists.models import Item
from django.shortcuts import redirect
# Create your views here.
def home_page(request):
    if request.method == 'POST':
        # new_item_text = request.POST['item_text']
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')
    items = Item.objects.all()
    return  render(request, 'home.html',{'items':items})