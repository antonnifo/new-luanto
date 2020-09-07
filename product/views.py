from django.shortcuts import render, get_object_or_404
from .models import Product, Category, ProductImage
from django.db.models import Count
from cart.forms import CartAddProductForm


PRODUCTS = Product.is_available.all()
def index(request):
    
    
    return render(request,
        'product/index.html', {
            'trending': PRODUCTS[:8]
        })


def product_list(request, category_slug=None):
 
    def get_category(name):
        return Category.objects.filter(name=name)

    products   = PRODUCTS

    category   = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
   
    return render(request,
      'product/product_list.html',
      {
        "products" : products,
        "Men": get_category('Men'),
        "Women": get_category('Women'),
        "Kids": get_category('Kids'),
        "Home": get_category('Home'),
        "category" : category

      })



def product_detail(request, id, slug):

    product = get_object_or_404(Product,
                            id=id,
                            slug=slug,
                            available=True)

    # related products
     
    product_tags_ids = product.tags.values_list('id', flat=True)
    
    related_products = PRODUCTS.filter(tags__in=product_tags_ids)\
                        .exclude(id=product.id)

    related_products = related_products.annotate(same_tags=Count('tags')).order_by('-same_tags','-updated')[:4]
    cart_product_form = CartAddProductForm()
    return render(request,
              'product/product_detail.html',
              {
                  'product': product, 
                  'product_images': ProductImage.objects.filter(product=product),
                  'tags': product.tags.all(),
                  'related_products' :  related_products,
                  'cart_product_form': cart_product_form,            
               })
