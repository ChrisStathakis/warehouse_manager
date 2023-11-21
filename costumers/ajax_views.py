from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse

from .models import PaymentInvoice, InvoiceItem, CostumerDetails, Product
from .forms import CreateInvoiceItemForm, CostumerDetailsForm, CostumerForm


@staff_member_required
def costumer_create_popup_view(request):
    form = CostumerForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_costumer");</script>' % (instance.pk, instance))

    return render(request, "form_view.html", context=locals())


@staff_member_required
def ajax_create_item(request, pk):
    instance = get_object_or_404(PaymentInvoice, id=pk)
    form = CreateInvoiceItemForm(request.POST or None, initial={'invoice': instance})
    if form.is_valid():
        data = form.save()
        product = Product.objects.create(
            title=form.cleaned_data.get('title', 'No data'),
            value=form.cleaned_data.get('sell_price', 0),
            value_discount=0,
            final_value=0,
        )
        data.product = product
        data.save()


    instance.refresh_from_db()
    data = dict()
    data['result'] = render_to_string(template_name='costumers/ajax/order_items.html',
                                      request=request,
                                      context={'object': instance})
    data['details'] = render_to_string(template_name='costumers/ajax/order_details.html',
                                       request=request,
                                       context={
                                           'object': instance
                                       }
                                       )
    return JsonResponse(data)


@staff_member_required
def ajax_delete_order_item(request, pk):
    instance = get_object_or_404(InvoiceItem, id=pk)
    order = instance.invoice
    instance.delete()
    order.refresh_from_db()
    data = dict()
    data['result'] = render_to_string(template_name='costumers/ajax/order_items.html',
                                      request=request,
                                      context={
                                          'object': order
                                      }
                                      )
    data['details'] = render_to_string(template_name='costumers/ajax/order_details.html',
                                       request=request,
                                       context={
                                           'object': order
                                       }
                                       )
    return JsonResponse(data)


@staff_member_required
def update_costumer_detail_view(request, pk):
    instance = get_object_or_404(CostumerDetails, id=pk)
    form = CostumerDetailsForm(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save()
        instance.costumer.update_costumer_data_from_form(obj)
    else:
        print(form.errors)
    return redirect(instance.invoice.get_edit_url())


