from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver

from .models import Payment, Invoice,  InvoiceItem


@receiver(post_delete, sender=Payment)
def update_vendor_on_delete(sender, instance, **kwargs):
    instance.vendor.update_paid_value()


@receiver(pre_delete, sender=Invoice)
def update_products_on_invoice_delete(sender, instance, **kwargs):
    for item in instance.order_items:
        item.delete()


@receiver(post_delete, sender=Invoice)
def update_vendor_invoice_on_delete(sender, instance, **kwargs):
    instance.vendor.update_value()


@receiver(post_delete, sender=InvoiceItem)
def update_anything_on_order_item_delete(sender, instance, **kwargs):
    instance.invoice.save()
    instance.product.save()
