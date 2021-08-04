from django.shortcuts import get_object_or_404

from .models import Category ,Product

def menu_links(request):
    links = Category.objects.all()
    products = Product.objects.all()
    return dict(links=links,products=products)
