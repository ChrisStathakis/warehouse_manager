from django.shortcuts import render
from functools import reduce
from django.db.models import Q
from django.shortcuts import get_object_or_404
from operator import or_
from django.template.loader import render_to_string
from django.http import JsonResponse
from products.models import Product, Category, PriceList


def public_product_view(request):
    qs = Product.filters_data(request, Product.objects.filter(active=True))[:100]
    categories = PriceList.objects.all()
    return render(request, 'public/index.html', context={'qs': qs, 'categories': categories})


def public_category_products_view(request, pk):
    instance = get_object_or_404(PriceList, id=pk)
    categories = PriceList.objects.filter(active=True)
    qs = Product.objects.filter(price_list=instance)
    return render(request, 'public/index.html', context={'qs': qs, 'categories': categories})


def ajax_search_products(request):
    data = dict()
    search_name = request.GET.get('search_name', None)
    qs = Product.objects.none()
    if len(search_name) > 2:
        q = search_name.split(" ")
        print('q', q)
        qs = Product.objects.filter(
           reduce(
               or_,
               (
                   Q(title__icontains=sq) for sq in q
               )

            )
        ).distinct()
    data['result'] = render_to_string(template_name='public/ajax_products.html', request=request, context={'qs': qs})
    return JsonResponse(data)


