from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.db.models import F, Sum, FloatField
from django_tables2.tables import RequestConfig

from .models import Product, Category, ProductVendor, TAXES_CHOICES, PriceList
from .forms import ProductFrontEndForm, ProductVendorFrontEndform, PriceListForm
from vendors.models import Vendor, InvoiceItem
from costumers.models import InvoiceItem as SellInvoiceItem
from .tables import CategoryTable, ProductTable, PriceTable
from frontend.tools import build_url


@staff_member_required
def update_product_fpa_view(request):
    qs = Product.objects.filter(taxes_modifier='c')
    for product in qs:
        new_qty = product.qty/2 if product.qty %2 == 0 else int(product.qty/2)
        product.qty = new_qty
        product.save()
    
    return redirect('/')


@staff_member_required
def manipulate_apografi_view(request):
    qs = Product.filters_data(request, Product.objects.all())
    total_value = qs.aggregate(total=Sum(F('price_buy') * F('qty')),)['total'] if qs.exists() else 0
    taxes_value = []
    taxes_value = [
        ['24 %', qs.filter(taxes_modifier='c').aggregate(total=Sum(F('price_buy') * F('qty')),)['total'] if qs.filter(taxes_modifier='c').exists() else 0],
        ['13 %', qs.filter(taxes_modifier='b').aggregate(total=Sum(F('price_buy') * F('qty')),)['total'] if qs.filter(taxes_modifier='b').exists() else 0],
        ['6 %', qs.filter(taxes_modifier='d').aggregate(total=Sum(F('price_buy') * F('qty')),)['total'] if qs.filter(taxes_modifier='d').exists() else 0],
        ['0 %', qs.filter(taxes_modifier='a').aggregate(total=Sum(F('price_buy') * F('qty')),)['total'] if qs.filter(taxes_modifier='a').exists() else 0],
    ]
    
    return render(request, 'products/apografi.html', context=locals())


@method_decorator(staff_member_required, name='dispatch')
class ProductHomepageView(TemplateView):
    template_name = 'products/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['vendors'] = Vendor.objects.all()
        return context


@method_decorator(staff_member_required, name='dispatch')
class ProductListView(ListView):
    template_name = 'products/products_list.html'
    model = Product
    paginate_by = 50
    total_products = 0

    def get_queryset(self):
        # need fixing
        products = Product.objects.all()
        qs = Product.filters_data(self.request, products)
        vendors = Vendor.filters_data(self.request, Vendor.objects.all())
        vendor_qs = vendors.values_list('id')
        items = InvoiceItem.objects.filter(vendor__id__in=vendor_qs)
        items_ids = items.values_list("product__id")
        qs = qs.filter(id__in=items_ids) if items_ids else qs
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset_table = ProductTable(self.object_list)
        RequestConfig(self.request).configure(queryset_table)
        context.update(locals())
        return context

    
@method_decorator(staff_member_required, name='dispatch')
class ProductEditListView(ListView):
    model = Product
    template_name = 'products/list_view.html'
    paginate_by = 50

    def get_queryset(self):
        qs = Product.filters_data(self.request, Product.objects.all())
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset_table = ProductTable(self.object_list)
        RequestConfig(self.request).configure(queryset_table)
        context["page_title"] = 'Λιστα Προϊόντων'
        context['queryset_table'] = queryset_table
        context['back_url'] = reverse('vendors:home')
        context['create_url'] = reverse('edit_product_create')
        context['categories'] = Category.objects.all()
        context['search_filter'], context['category_filter'], context['check_vendor_filter'] = [True]*3
        return context


@method_decorator(staff_member_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductFrontEndForm
    template_name = 'form_view.html'

    def get_success_url(self):
        return self.new_product.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = 'Δημιουργια Προϊόντος'
        context["back_url"] = reverse('edit_product_list')  
        return context

    def form_valid(self, form):
        self.new_product = form.save()
        return super().form_valid(form)
    

@method_decorator(staff_member_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductFrontEndForm
    template_name = 'products/product_update_view.html'

    def get_success_url(self):
        return self.object.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f'{self.object}'
        context['product_vendor_form'] = ProductVendorFrontEndform(initial={'product': self.object})
        context['action_url'] = reverse('edit_product_list')
        invoice_qs = self.object.invoice_vendor_items.all()
        sell_qs = self.object.sell_items.all()
        invoice_qs = InvoiceItem.filters_data(request=self.request, qs=invoice_qs)
        sell_qs = SellInvoiceItem.filters_data(self.request, sell_qs)
        context['vendor_invoices'] = invoice_qs
        context['sell_invoices'] = sell_qs
        context['date_filter'] = True
        return context


@staff_member_required
def delete_product_view(request, pk):
    instance = get_object_or_404(Product, id=pk)
    instance.delete()
    messages.success(request, f'Το Προϊον {instance.title} διαγραφηκε')
    return redirect(reverse('edit_product_list'))


@staff_member_required
def copy_product_view(request, pk):
    instance = get_object_or_404(Product, id=pk)
    instance.pk = None
    instance.save()
    messages.success(request, 'Το Προιόν αντιγραφηκε επιτυχώς.')
    return redirect(instance.get_edit_url())
    

@method_decorator(staff_member_required, name='dispatch')
class ProductVendorUpdateView(UpdateView):
    model = ProductVendor
    form_class = ProductVendorFrontEndform
    template_name = 'form_view.html'

    def get_success_url(self):
        return self.object.product.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super(ProductVendorUpdateView, self).get_context_data(**kwargs)
        context['form_title'] = f'Επεξεργασια {self.object}'
        context['back_url'] = self.get_success_url()
        context['delete_url'] = self.object.get_delete_url()
        return context


@staff_member_required
def product_vendor_delete_view(request, pk):
    instance = get_object_or_404(ProductVendor, id=pk)
    instance.delete()
    messages.success(request, f'Το προϊον {instance} διαγραφηκε.')
    return redirect(instance.product.get_edit_url())


@staff_member_required
def create_product_vendor_view(request, pk):
    product = get_object_or_404(Product, id=pk)
    form = ProductVendorFrontEndform(request.POST or None, initial={'product': product})
    if form.is_valid():
        form.save()
        return redirect(product.get_edit_url())
    else:
        print(form.errors)
    return redirect(product.get_edit_url())


# --down here


@method_decorator(staff_member_required, name='dispatch')
class PriceListView(ListView):
    template_name = 'list_view.html'
    model = PriceList
    paginate_by = 50
    total_products = 0

    def get_queryset(self):
        qs = PriceList.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset_table = PriceTable(self.object_list)
        RequestConfig(self.request).configure(queryset_table)
        context['create_url'] = self.model.get_create_url()
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class PriceListCreateView(CreateView):
    model = PriceList
    form_class = PriceListForm
    template_name = 'form_view.html'

    def get_success_url(self):
        return self.new_product.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = 'Δημιουργια Τιμοκαταλόγου'
        context["back_url"] = reverse('price_list_view')
        return context

    def form_valid(self, form):
        self.new_product = form.save()
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class PriceListUpdateView(UpdateView):
    model = PriceList
    form_class = PriceListForm
    template_name = 'products/price_detail_view.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f'{self.object}'
        context['products'] = Product.objects.all()[:100]
        context['qs'] = Product.objects.filter(price_list=self.object)
        context["create_product"] = ProductFrontEndForm()
        return context


@staff_member_required
def delete_price_list_view(request, pk):
    instance = get_object_or_404(PriceList, id=pk)
    instance.delete()
    messages.success(request, f'The price list {instance.title} διαγραφηκε')
    return redirect(reverse('price_list_detail'))


@staff_member_required
def print_price_list_view(request, pk):
    instance = get_object_or_404(PriceList, id=pk)
    products = Product.objects.filter(price_list=instance)
    return render(request, "costumers/print/price_list_print_view.html", context={"instance": instance, "qs": products})
