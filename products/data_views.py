import unidecode
import re
from import_export import resources
from django.http import HttpResponse

from .models import Product, Category, ProductVendor


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product


class CategoryResource(resources.ModelResource):

    class Meta:
        model = Category


class ProductVendorResource(resources.ModelResource):

    class Meta:
        model = ProductVendor


def backup_products_view(request):
    data = ProductResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="products.xls"'
    return response


def backup_products_vendor_view(request):
    data = ProductVendorResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="products_vendor.xls"'
    return response


def backup_categories_view(request):
    data = CategoryResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="product_categories.xls"'
    return response


def filter_greek_words(word):
    greek_pattern = re.compile(r'^[Α-Ωα-ωάέήίόύώΆΈΉΊΌΎΏ]+$', re.UNICODE)
    return unidecode.unidecode(word, 'Greek') if greek_pattern else word


def fix_products_titles_view(request):
    qs = Product.objects.all()
    for ele in qs:
        new_string = f'{ele.title}'.upper()
        new_string_list = new_string.split(" ")
        fixed_string = []
        for word in new_string_list:
            if "Έ" in word:
                word = word.replace("Έ", "Ε")
            if "Ά" in word:
                word = word.replace("Ά", "Α")
            if "Ί" in word:
                word = word.replace("Ί", "Ι")
            if "Ή" in word:
                word = word.replace("Ή", "Η")
            if "Ύ" in word:
                word = word.replace("Ύ", "Υ")
            if "Ό" in word:
                word = word.replace("Ό", "Ο")
            if "Ώ" in word:
                word = word.replace("Ώ", "Ω")
            fixed_string.append(word)
        ele.title = ' '.join(fixed_string)

        ele.save()
        print(ele.title)
