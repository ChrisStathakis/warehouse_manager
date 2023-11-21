from django.urls import path

from .views import (
    PaymentInvoiceListView, PaymentInvoiceCreateView, PaymentInvoiceUpdateView, print_invoice_view,
                    PaymentInvoiceCreateFromOrderView, locked_invoice_view, delete_payment_invoice, test_xml,
                    add_product_to_invoice_action_view, update_invoice_item_view,
                    )
from .autocomplete_views import ProductAutocompleteView
from .create_xmls import InvoiceViewSet
from .ajax_views import (ajax_create_item, update_costumer_detail_view, ajax_delete_order_item,
                         costumer_create_popup_view,
                         )
app_name = 'costumers'

urlpatterns = [
    path('home/', PaymentInvoiceListView.as_view(), name='home'),
    path('payment-invoice-create/', PaymentInvoiceCreateView.as_view(), name='payment_invoice_create'),
    path('payment-invoice-create-from-costumer/<int:pk>', PaymentInvoiceCreateFromOrderView.as_view(),
         name='payment_invoice_create_costumer'),
    path('payment-update/<int:pk>/', PaymentInvoiceUpdateView.as_view(), name='payment_invoice_update'),
    path('payment-item-update/<int:pk>/', update_invoice_item_view, name='payment-item-update'),
    path('costumer-popup-view/', costumer_create_popup_view, name='costumer_create_popup'),

    path('ajax/create/<int:pk>/', ajax_create_item, name='ajax_create_item'),
    path('ajax/delete/<int:pk>/', ajax_delete_order_item, name='ajax_delete_order_item'),
    path('print/<int:pk>/', print_invoice_view, name='print_invoice'),
    path('update-invoice-profile/<int:pk>/', update_costumer_detail_view, name='update_invoice_profile'),

    path('add-product-to-invoice/<int:pk>/<int:dk>/', add_product_to_invoice_action_view, name='add_product_to_invoice'),
    path('add-product-to-invoice/<int:pk>/<int:dk>/', add_product_to_invoice_action_view, name='add_product_to_invoice'),

    path('payment-invoice-delete/<int:pk>/', delete_payment_invoice, name='delete_payment_invoice'),
    path('lnvoice/locked/<int:pk>', locked_invoice_view, name='invoice_locked'),
    path('test/', test_xml),
    path('invoice-xml/', InvoiceViewSet.as_view(['list', 'get'])),
    path('autocomplete-products/', ProductAutocompleteView.as_view(), name='autocomplete_products'),

]
