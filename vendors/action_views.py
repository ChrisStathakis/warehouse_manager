from django.shortcuts import render, reverse, get_object_or_404, HttpResponseRedirect, redirect
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from importlib_metadata import requires

from products.models import ProductVendor, Product
from products.forms import ProductClassForm
from .models import Vendor, Invoice, Payment, Employer, PaymentMethod, VendorBankingAccount, Note, InvoiceItem
from .forms import (InvoiceVendorDetailForm, EmployerForm, PaymentForm, InvoiceForm, VendorBankingAccountForm, NoteForm,
                    VendorProductForm, ProductVendorClassForm, CopyProductToNewVendor, CopyProductFromVendorCardForm,
                    PaycheckForm, InvoiceItemForm, InvoiceProductForm
                    )


@staff_member_required
def validate_paycheck_form_view(request, pk):
    vendor = get_object_or_404(Vendor, id=pk)
    form = PaycheckForm(request.POST or None, initial={'vendor': vendor})
    if form.is_valid():
        instance = form.save()
        messages.success(request, f'Η επιταγή {instance.title} δημιουργήθηκε επιτυχώς')
    else:
        messages.warning(request, 'δημιουργήθηκε κάποιο πρόβλημα')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    


@staff_member_required
def validate_invoice_form_view(request, pk):
    vendor = get_object_or_404(Vendor, id=pk)
    form = InvoiceVendorDetailForm(request.POST or None, initial={'vendor': vendor})
    if form.is_valid():
        new_instance = form.save()
        messages.success(request, f'Το παραστατικό {new_instance.title} δημιουργηθηκε.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_payment_form_view(request, pk):
    vendor = get_object_or_404(Vendor, id=pk)
    form = PaymentForm(request.POST or None, initial={'vendor': vendor})
    if form.is_valid():
        new_instance = form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_employer_view(request, pk):
    vendor = get_object_or_404(Vendor, id=pk)
    form = EmployerForm(request.POST or None, initial={'vendor': vendor})
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_invoice_edit_form_view(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    form = InvoiceForm(request.POST or None, instance=invoice)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def delete_invoice_view(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    invoice.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_payment_edit_form_view(request, pk):
    invoice = get_object_or_404(Payment, id=pk)
    form = PaymentForm(request.POST or None, instance=invoice)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def delete_payment_view(request, pk):
    invoice = get_object_or_404(Payment, id=pk)
    invoice.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_employer_edit_view(request, pk):
    employer = get_object_or_404(Employer, id=pk)
    form = EmployerForm(request.POST or None, instance=employer)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def delete_employer_view(request, pk):
    employer = get_object_or_404(Employer, id=pk)
    employer.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_create_banking_account_view(request, pk):
    vendor = get_object_or_404(Vendor, id=pk)
    form = VendorBankingAccountForm(request.POST, initial={'vendor': vendor})
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_edit_banking_account_view(request, pk):
    banking_account = get_object_or_404(VendorBankingAccount, id=pk)
    form = VendorBankingAccountForm(request.POST or None, instance=banking_account)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def delete_banking_account_view(request, pk):
    banking_account = get_object_or_404(VendorBankingAccount, id=pk)
    banking_account.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_note_creation_view(request, pk):
    instance = get_object_or_404(Vendor, id=pk)
    form = NoteForm(request.POST or None, initial={'vendor_related': instance})
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_product_creation_view(request, pk):
    instance = get_object_or_404(Vendor, id=pk)
    form = VendorProductForm(request.POST or None)
    if form.is_valid():
        product = form.save()
        value = form.cleaned_data.get('warehouse_value', 0)
        discount = form.cleaned_data.get('discount', 0)
        extra_value = form.cleaned_data.get('extra_value', 0)
        taxes_modifier = form.cleaned_data.get('taxes_modifier', 'c')
        is_favorite = form.cleaned_data.get('is_favorite', False)
        sku_ware = form.cleaned_data.get('sku_ware', '')
        new_vendor = ProductVendor.objects.create(
            product=product,
            vendor=instance,
            value=value,
            discount=discount,
            added_value=extra_value,
            taxes_modifier=taxes_modifier,
            is_favorite=is_favorite,
            sku=sku_ware

        )
        messages.success(request, f'Το Προϊόν {product.title} δημιουργήθηκε. Στοιχεια:  Τιμή Αγόρας..{value} '
                                  f' Εκπτωση..{discount} Επιπλεον Αξία..{extra_value}'
                         )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_product_edit_view(request, pk):
    product = get_object_or_404(Product, id=pk)
    form = ProductClassForm(request.POST, instance=product)
    if form.is_valid():
        form.save()
        messages.success(request, f'Το προϊόν {product} επεξεργαστηκε επιτυχώς')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_product_vendor_edit_view(request, pk):
    instance = get_object_or_404(ProductVendor, id=pk)
    form = ProductVendorClassForm(request.POST, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, f'Το  προϊόν {instance} του προμηθευτη {instance.vendor} επεξεργαστηκε επιτυχώς')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def copy_product_to_new_vendor(request, pk):
    instance = get_object_or_404(ProductVendor, id=pk)
    form = CopyProductToNewVendor(request.POST or None,
                                  initial={'value': instance.value,
                                           'discount': instance.discount, 
                                           'added_value': instance.added_value
                                            })
    form_title = f'Αντιγραφή Προϊόντος {instance.product}'
    back_url = instance.vendor.get_card_url()
    if form.is_valid():
        new_product_vendor = ProductVendor.objects.create(
            product=instance.product,
            vendor=form.cleaned_data['vendor'],
            value=form.cleaned_data['value'],
            discount=form.cleaned_data['discount'],
            added_value=form.cleaned_data['added_value']
        )
        return HttpResponseRedirect(instance.vendor.get_card_url())
    context = locals()
    return render(request, 'form_view.html', context)


def copy_product_from_vendor_card_view(request, pk, dk):
    instance = get_object_or_404(Product, id=pk)
    vendor = get_object_or_404(Vendor, id=dk)
    form = CopyProductFromVendorCardForm(request.POST or None, initial={
        'product': instance,
        'vendor': vendor
    })
    if form.is_valid():
        form.save()
        messages.success(request, 'Νεος Προμηθευτής Προστέθηκε')
        return redirect(vendor.get_card_url())
    return render(request, 'form_view.html', context=locals())


def action_favorite_view(request, pk):
    instance = get_object_or_404(ProductVendor, id=pk)
    instance.is_favorite = False if instance.is_favorite else True
    instance.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def action_form_copy_vendor_product_view(request, pk):
    product_vendor = get_object_or_404(ProductVendor, id=pk)
    product = product_vendor.product
    back_url = product_vendor.vendor.get_card_url()
    form_title = f'Αντιγραφή προϊόντος {product.title}'
    form = VendorProductForm(request.POST or None, 
                             initial={
                                 'vendor': product_vendor.vendor,
                                 'active': product.active,
                                 'is_favorite': product_vendor.is_favorite,
                                 'title': product.title,
                                 'sku': product.sku,
                                 'qty': product.qty,
                                 'categories': product.categories.all(),
                                 'sku_ware': product_vendor.sku,
                                 'warehouse_value': product_vendor.value,
                                 'discount': product_vendor.discount,
                                 'extra_value': product_vendor.added_value,
                                 'value': product.value,
                                 'taxes_modifier': product_vendor.taxes_modifier
                             })
    if form.is_valid():
        product = form.save()
        value = form.cleaned_data.get('warehouse_value', 0)
        discount = form.cleaned_data.get('discount', 0)
        extra_value = form.cleaned_data.get('extra_value', 0)
        taxes_modifier = form.cleaned_data.get('taxes_modifier', 'c')
        is_favorite = form.cleaned_data.get('is_favorite', False)
        sku_ware = form.cleaned_data.get('sku_ware', '')
        new_vendor = ProductVendor.objects.create(
            product=product,
            vendor=product_vendor.vendor,
            value=value,
            discount=discount,
            added_value=extra_value,
            taxes_modifier=taxes_modifier,
            is_favorite=is_favorite,
            sku=sku_ware

        )
        messages.success(request, f'Το Προϊόν {product.title} δημιουργήθηκε. Στοιχεια:  Τιμή Αγόρας..{value} '
                                  f' Εκπτωση..{discount} Επιπλεον Αξία..{extra_value}'
                         )
        return redirect(product_vendor.vendor.get_card_url())

    return render(request, 'form_view.html', context=locals())



@staff_member_required
def validate_create_invoice_order_item_view(request, pk):
    instance = get_object_or_404(Invoice, id=pk)
    form = InvoiceItemForm(request.POST or None, initial={'invoice': instance,
                                                          'vendor': instance.vendor,
                                                          })
    if form.is_valid():
        data = form.save()
        product = data.product
        product.price_buy = data.value
        product.order_sku = data.order_code
        product.order_discount = data.discount
        product.save()


    else:
        print(form.errors)
    return redirect(instance.get_edit_url())


@staff_member_required
def validate_order_item_update_view(request, pk):
    instance = get_object_or_404(InvoiceItem, id=pk)
    form = InvoiceItemForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()

    return redirect(instance.invoice.get_edit_url())


@staff_member_required
def delete_invoice_item_view(request, pk):
    instance = get_object_or_404(InvoiceItem, id=pk)
    instance.delete()
    return redirect(instance.invoice.get_edit_url())


@staff_member_required
def create_product_from_invoice(request, pk):
    instance = get_object_or_404(Invoice, id=pk)
    form = InvoiceProductForm(request.POST or None, initial={'vendor': instance.vendor,})
    if form.is_valid():
        product = form.save()
       
        qty = form.cleaned_data.get('qty', 1)
        new_item = InvoiceItem.objects.create(
                    order_code=product.order_code,
                    vendor=instance.vendor,
                    invoice=instance,
                    product=product,
                    unit=product.unit,
                    qty=qty,
                    value=product.price_buy,
                    discount=0,
                    taxes_modifier=product.taxes_modifier,
                    
                )

        
        return redirect(instance.get_edit_url())
    else:
        messages.warning(request, form.errors)
    return redirect(instance.get_edit_url())