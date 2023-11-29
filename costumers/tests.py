from django.test import TestCase

import datetime
# Create your tests here.
from .models import  PaymentInvoice, Product, UNITS, Costumer
from .models import InvoiceItem as SellInvoiceItem
from vendors.models import Vendor, Invoice, InvoiceItem


class InvoiceQtyTestCase(TestCase):

    def setUp(self) -> None:
        vendor = Vendor.objects.create(title="test-vendor", value=0, paid_value=0, )
        self.product = Product.objects.create(title="product1", value=0)
        self.customer = Costumer.objects.create(eponimia="title", paid_value=0, value=0)
        product = self.product
        invoice1 = Invoice.objects.create(vendor=vendor, date=datetime.datetime(2023, 1, 6), value=0, extra_value=0)
        invoice2 = Invoice.objects.create(vendor=vendor, date=datetime.datetime(2023, 1, 18), value=0, extra_value=0)
        self.invoice_item1 = InvoiceItem.objects.create(vendor=vendor, invoice=invoice1, product=product, discount=0, value=50, qty=4)
        self.invoice_item2 = InvoiceItem.objects.create(vendor=vendor, invoice=invoice2, product=product, discount=0, value=60, qty=6)

    def test_qty(self):
        # initial
        self.assertEqual(10, self.product.qty)
        self.assertEqual(56, self.product.average_price)

        # check warehouse movement
        sell_invoice = PaymentInvoice.objects.create(date=datetime.datetime.now(), costumer=self.customer)
        sell_invoice_item = SellInvoiceItem.objects.create(invoice=sell_invoice, product=self.product, qty=5)
        self.assertEqual(5, self.product.qty)
        self.assertEqual(56, self.product.average_price)

        # third part: calculate qty
        self.emulate_locking_progression(sell_invoice)
        #self.assertEqual(2, self.invoice_item1.remaining_qty)
        # self.assertEqual(58.33, self.product.average_price)
        self.assertEqual(0, self.invoice_item1.remaining_qty)


    def emulate_locking_progression(self, instance: PaymentInvoice):
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
                            
                





               

        