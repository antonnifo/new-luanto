from django.shortcuts import render, get_object_or_404
from .models import Product, Category, ProductImage


PRODUCTS = Product.is_available.all()
def index(request):
    
    
    return render(request,
        'product/index.html', {
            'trending': PRODUCTS[:8]
        })


def product_list(request):

   
    return render(request,
      'product/product_list.html',
      {"products" : PRODUCTS})

def product_detail(request, id, slug):

    product = get_object_or_404(Product,
                            id=id,
                            slug=slug,
                            available=True)

    return render(request,
              'product/product_detail.html',
              {
                  'product': product,              
               })
