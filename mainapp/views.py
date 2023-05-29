from django.shortcuts import render
from .models import Item
from django.views.generic import View, DetailView, ListView


# Create your views here.
# def index(request):
#    context = {
#        'items': Item.objects.all()
#    }
#    return render(request, 'index.html', context=context)


class IndexView(ListView):
    model = Item
    paginate_by = 10
    template_name = 'index.html'


class ProductDetailView(DetailView):
    model = Item
    template_name = 'product.html'
