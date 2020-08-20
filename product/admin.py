import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse

from .models import Category, Product, ProductImage


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;'\
        'filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many
              and not field.one_to_many]

    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ['id', 'slug', 'name', 'sub_category']
    prepopulated_fields = {'slug': ('sub_category',)}
    list_editable = ['name','sub_category']


class ProducImageInline(admin.TabularInline):

    model = ProductImage
    raw_id_fields = ['product']
    


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ['name', 'original_price', 'discount_price',
                    'available', 'category', 'updated','on_offer']
    list_filter = ['available', 'category', 'updated']
    list_editable = ['original_price', 'discount_price', 'available','on_offer']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProducImageInline]
    actions = [export_to_csv]
    list_per_page = 5

admin.site.site_header = "LUANTOO" 