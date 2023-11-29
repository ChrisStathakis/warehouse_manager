from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum

from django.template.loader import render_to_string
import os
from django.conf import settings
BASE_DIR = settings.BASE_DIR
import requests


from .models import PaymentInvoice, MyCard, InvoiceItem, CostumerDetails
from orders.models import Order, Costumer
from .tables import PaymentInvoiceTable
import http.client, urllib.request, urllib.parse, urllib.error, base64
from .forms import PaymentInvoiceForm, CostumerDetailsForm, CreateInvoiceItemForm, PaymentInvoiceEditForm, UpdateInvoiceItemForm
from .api_methods import send_invoices
from products.models import Product


@method_decorator(staff_member_required, name='dispatch')
class PaymentInvoiceListView(ListView):
    template_name = 'list_view.html'
    model = PaymentInvoice

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['queryset_table'] = PaymentInvoiceTable(self.object_list)
        context['create_url'] = reverse('costumers:payment_invoice_create')
        context['back_url'] = reverse('costumer_homepage')
        context['costumers'] = Costumer.objects.filter(active=True)
        context['costumers_filter'] = True
        return context


@method_decorator(staff_member_required, name='dispatch')
class PaymentInvoiceCreateView(CreateView):
    template_name = 'form_view.html'
    model = PaymentInvoice
    form_class = PaymentInvoiceForm

    def get_initial(self):
        initial = super().get_initial()
        fav_card = MyCard.objects.filter(favorite=True)
        if fav_card.exists():
            initial['card_info'] = fav_card.first()
        return initial

    def get_success_url(self):
        return self.new_instance.get_edit_url()

    def form_valid(self, form):
        self.new_instance = form.save()
        return super(PaymentInvoiceCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Δημιουργια Παραστατικου'
        context['back_url'] = reverse('costumers:home')
        context['costumer_popup'] = True
        return context


@method_decorator(staff_member_required, name='dispatch')
class PaymentInvoiceCreateFromOrderView(CreateView):
    template_name = 'form_view.html'
    model = PaymentInvoice
    form_class = PaymentInvoiceForm

    def get_initial(self):
        costumer = get_object_or_404(Costumer, id=self.kwargs['pk'])
        initial = super().get_initial()
        fav_card = MyCard.objects.filter(favorite=True)
        if fav_card.exists():
            initial['card_info'] = fav_card.first()
        initial['costumer'] = costumer
        return initial

    def get_success_url(self):
        return self.new_instance.get_edit_url()

    def form_valid(self, form):
        self.new_instance = form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Δημιουργια Παραστατικου'
        context['back_url'] = reverse('costumers:home')

        return context


@method_decorator(staff_member_required, name='dispatch')
class PaymentInvoiceUpdateView(UpdateView):
    # template_name = 'costumers/update_invoice.html'
    model = PaymentInvoice
    form_class = PaymentInvoiceEditForm

    def get_template_names(self):
        return 'costumers/update_deltio_pa.html' if self.object.order_type == 'd' else 'costumers/update_invoice.html'

    def get_success_url(self):
        return self.object.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.filters_data(self.request, Product.objects.filter(active=True))[:30]
        profile = CostumerDetails.objects.filter(invoice=self.object).first()
        if profile:
            context['costumer_form'] = CostumerDetailsForm(self.request.POST or None, instance=profile)
        else:
            context['costumer_form'] = CostumerDetailsForm(self.request.POST or None)
        context['item_form'] = CreateInvoiceItemForm(self.request.POST or None, initial={'invoice': self.object})
        qs = Order.objects.filter(favorite=True)
        context['order'] = qs.first() if qs.exists() else None
        return context

    def form_valid(self, form):
        form.save()
        return super(PaymentInvoiceUpdateView, self).form_valid(form)


@staff_member_required
def add_product_to_invoice_action_view(request, pk, dk):
    instance = get_object_or_404(PaymentInvoice, id=pk)
    product = get_object_or_404(Product, id=dk)
    form = UpdateInvoiceItemForm(request.POST or None, initial={
        'product': product,
        'invoice': instance,
        'sell_price': product.final_value,

    })
    back_url, form_title = instance.get_edit_url(), f'{product.title}'
    if form.is_valid():
        new_item = form.save()
        product.value = form.cleaned_data.get('sell_price', 0)
        product.save()
        return redirect(instance.get_edit_url())
    return render(request, 'form_view.html', context=locals())


@staff_member_required()
def update_invoice_item_view(request, pk):
    instance = get_object_or_404(InvoiceItem, id=pk)
    product = instance.product
    detail_form = True
    form = UpdateInvoiceItemForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect(instance.invoice.get_edit_url())
    back_url = instance.invoice.get_edit_url()
    return render(request, 'form_view.html', context=locals())


@staff_member_required()
def print_invoice_view(request, pk):
    instance = get_object_or_404(PaymentInvoice, id=pk)
    costumer = instance.profile
    card = instance.card_info
    total_qty = instance.order_items.aggregate(Sum('qty'))['qty__sum'] if instance.order_items.exists() else 0
    different_taxes = instance.order_items.values('taxes_modifier').annotate(
        total_taxes=Sum('taxes_value'),
        total_clean=Sum('clean_value'),
        total=Sum('total_value')
    ).order_by('taxes_modifier')
    
    for item in different_taxes:
        if item['taxes_modifier'] == 'b':
            item['taxes_modifier'] = '13%'
        elif item['taxes_modifier'] == 'c':
            item['taxes_modifier'] = '24%'
        else:
            item['taxes_modifier'] = '6%'
    return render(request, 'costumers/print/index.html', {'instance': instance,
                                                          'costumer': costumer,
                                                          'card_info': card,
                                                          'different_taxes': different_taxes,
                                                          'total_qty': total_qty
                                                          })



def test_xml(request):
    instance = PaymentInvoice.objects.last()
    order_items = instance.order_items
    headers, params = send_invoices(instance)
    context = {
        'instance': instance,
        'order_items': order_items,
        'profile': instance.profile,
        'card': instance.card_info
    }
    content = render_to_string('costumers/test.xml', context)
    print('first phase')
    with open(os.path.join(BASE_DIR, 'static/test.xml'), 'w') as xmlfile:
        xmlfile.write(content)
        xmlfile.close()
    print('second phase')

    with open(os.path.join(BASE_DIR, 'static/test.xml'), 'r') as read_file:
        print('before reque', read_file)
        response = requests.post("https://mydata-dev.azure-api.net/myDATAProvider/SendInvoices", data=read_file, headers=headers)
        print('response', response)
        xmlfile.close()

    return render(request, 'costumers/test.xml', context)


@staff_member_required
def locked_invoice_view(request, pk):
    instance = get_object_or_404(PaymentInvoice, id=pk)
    if not instance.order_items.exists():
        messages.warning(request, 'Δεν εχετε προσθεσει προιοντα')
        return redirect(instance.get_edit_url())

    instance.locked = True
    # instance.save()
    '''
    headers, params = send_invoices(instance)


    try:
        conn = http.client.HTTPSConnection('mydata-dev.azure-api.net')
        conn.request("POST", "/SendInvoices?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        print('conn', conn)
        conn.close()
        print('data', data)
    except Exception as e:
        print('error', e)
        messages.warning(request, e)
    '''
    instance.save()
    # this is extra, trying to remove automatically the qty

    for item in instance.order_items.all():
        invoices = item.product.invoice_vendor_items.filter(remaining_qty__gt=0)
        quantity_to_sell = item.qty
        for invoice in invoices.order_by("date"):
            if quantity_to_sell > 0:
                if invoice.remaining_qty >= quantity_to_sell:
                    invoice.used_qty += quantity_to_sell
                    invoice.save()
                    quantity_to_sell = 0
                else:
                    invoice.used_qty += invoice.remaining_qty
                    quantity_to_sell -=  invoice.remaining_qty
                    invoice.save()
 
    return redirect(instance.get_edit_url())


@staff_member_required
def delete_payment_invoice(request, pk):
    instance = get_object_or_404(PaymentInvoice, id=pk)
    if instance.locked:
        messages.warning(request, 'Δε μπορει να διαγραφει αυτο το παραστατικο')
    else:
        instance.profile.delete()
        for ele in instance.order_items.all():
            ele.delete()
        instance.delete()
        messages.success(request, 'Το Παραστατικο Διαγραφηκε')
    return redirect('costumers:home')
