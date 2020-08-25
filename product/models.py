from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager

class AvailableManager(models.Manager):
    def get_queryset(self):
        return super(AvailableManager,
                     self).get_queryset().filter(available=True)
class Category(models.Model):

        CATEGORY_CHOICES  = (
            ("Men","Men"),
            ("Women","Women"),         
            ("Kids","Kids"),         
            ("Home","Home"),         
                 
        )
        name = models.CharField(max_length=200,
                db_index=True, choices=CATEGORY_CHOICES)
                
        sub_category = models.CharField(max_length=200, db_index=True) 
        slug = models.SlugField(max_length=200,
                    unique=True)

        image = models.ImageField(upload_to='category/', blank=True, null=True)


        class Meta:
            ordering = ('name',)
            verbose_name = 'category'
            verbose_name_plural = 'categories'

        def __str__(self):
            return self.sub_category

        def get_absolute_url(self):
            return reverse('product:product_list_by_category',
               args=[self.slug])


class Product(models.Model):

    is_available   = AvailableManager()
    tags = TaggableManager()

    category    = models.ForeignKey(Category,
                    related_name='products',
                            on_delete=models.CASCADE)
    name        = models.CharField(max_length=200, db_index=True)
    slug        = models.SlugField(max_length=200, db_index=True)
    sku         = models.CharField(max_length=200)
    photo       = models.ImageField(upload_to='products/%Y/%m/%d',
                                 blank=True)                                
    description = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    available   = models.BooleanField(default=True)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    def discount(self):
        """Return percent discount"""

        return  (self.original_price - self.discount_price)  * 100 // self.original_price
    class Meta:
        ordering       = ('name',)
        index_together = (('id', 'slug'),)
    
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:product_detail',
               args=[self.id, self.slug])


class ProductImage(models.Model):
    product = models.ForeignKey(Product,  on_delete=models.CASCADE)
    image   = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.product.name
