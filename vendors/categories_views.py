from django.shortcuts import render, redirect, reverse, HttpResponseRedirect

from django.contrib import messages
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse


from .tables import VendorTable
from products.models import Category, Product
from products.tables import CategoryTable, ProductTable, ProductTableForCategory
from products.forms import CategoryForm, ProductFrontEndForm
from .models import Vendor

from django_tables2 import RequestConfig


@method_decorator(staff_member_required, name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = 'list_view.html'

    def get_queryset(self):
        qs = Category.filters_data(self.request, Category.objects.all())
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'κατηγοριες'
        context['queryset_table'] = CategoryTable(self.object_list)
        context['create_url'] = reverse('vendors:category_create')
        context['back_url'] = reverse('vendors:home')
        return context


@method_decorator(staff_member_required, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'form_view.html'
    form_class = CategoryForm
    success_url = reverse_lazy('vendors:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'{self.object}'
        context['back_url'] = self.success_url
        context['delete_url'] = self.object.get_delete_url()
        print('gretretererg')
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    template_name = 'form_view.html'
    form_class = CategoryForm
    success_url = reverse_lazy('vendors:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Δημιουργια Κατηγορίας'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@staff_member_required
def category_delete_view(request, pk):
    instance = get_object_or_404(Category, id=pk)
    instance.delete()
    return redirect(reverse('vendors:category_list'))


@method_decorator(staff_member_required, name='dispatch')
class CategoryCardListView(ListView):
    model = Product
    template_name = 'categories/card_list.html'
    paginate_by = 50

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        qs = Product.objects.filter(categories=self.category)
        qs = Product.filters_data(self.request, qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super(CategoryCardListView, self).get_context_data(**kwargs)
        context['category'] = self.category
        context['back_url'] = reverse('vendors:category_list')
        qs_table = ProductTableForCategory(self.object_list)
        RequestConfig(self.request, paginate={"per_page": self.paginate_by}).configure(qs_table)
        context['queryset_table'] = qs_table
        vendors_ids = self.object_list.values_list('vendors')
        context['vendors'] = Vendor.objects.filter(id__in=vendors_ids)
        context['vendor_filter'], context['search_filter'] = 2*[True]
        context['create_product'] = ProductFrontEndForm(self.request.POST or None,
                                                          initial={'categories': self.category}
                                                          )
        context['products'] = Product.objects.all()[:100]
        context['qs'] = self.object_list
        return context


@staff_member_required
def print_category_products_view(request, pk):
    print('pk', pk)
    category = get_object_or_404(Category, id=pk)
    try:
        qs = Product.filters_data(request, Product.objects.filter(categories=category))
    except:
        qs = Product.objects.filter(categories=category)
    filtering = request.POST
    return render(request, 'costumers/print/category_print_view.html', context=locals())


