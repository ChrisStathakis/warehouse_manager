from django.urls import path

from .views import (homepage_vendor_view, VendorListApiView, InvoiceListApiView, VendorDetailApiView,
                    PaymentListCreateApiView, InvoiceRetrieveUpdateDeleteApiView
                    )


app_name = 'api_vendors'

urlpatterns = [
    path('', homepage_vendor_view, name='home'),
    path('list-create/', VendorListApiView.as_view(), name='list'),
    path('detail/<int:pk>/', VendorDetailApiView.as_view(), name='detail'),
    path('invoices/list/', InvoiceListApiView.as_view(), name='invoices'),
    path('invoices/update/<int:pk>/', InvoiceRetrieveUpdateDeleteApiView.as_view(), name='invoice_update'),
    path('payments/list/', PaymentListCreateApiView.as_view(), name='payments')
]