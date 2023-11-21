from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from analysis.data_views import backup_taxes_view
from costumers.data_views import (backup_invoice_items_view, backup_payments_invoices_view, backup_customers_view,
                                  backup_my_card_view, backup_customers_details_view
                                  )
from frontend.data_views import backup_payment_methods_view
from general_expenses.data_files import backup_general_expenses_folder_view, backup_general_expenses_category_folder_view
from incomes.data_views import backup_incomes_view
from notebook.data_views import backup_notebook_view, backup_tags_view
from orders.data_views import backup_orders_view, backup_orders_payment_view
from payroll.data_views import (backup_payrolls_view, backup_occupation_view, backup_bill_view,
                                backup_bill_categories_view,
                                backup_generic_expenses_category_view,
                                backup_generic_expenses_view,
                                backup_persons_view
                                )
from products.data_views import backup_products_view, backup_products_vendor_view, backup_categories_view
from vendors.data_views import backup_vendors_view, backup_vendor_notes_view, backup_vendor_employers_view, backup_vendor_payments_view, backup_vendor_banking_account_view, backup_invoices_view

urlpatterns = [

    path('backup/generic-expenses/', backup_vendors_view),
    path('backup/payrolls/', backup_vendor_notes_view),
    path('backup/occupation/', backup_vendor_employers_view),
    path('backup/bills/', backup_vendor_payments_view),
    path('backup/bill-categories/', backup_vendor_banking_account_view),
    path('backup/generic-expenses-category/', backup_invoices_view),


    path('admin/', admin.site.urls),
    path('costumers/', include('costumers.urls')),
    path('', include('frontend.urls')),
    path('warehouse/', include('vendors.urls')),
    path('products/', include('products.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('payrolls-and-bills/', include('payroll.urls')),
    path('incomes/', include('incomes.urls')),
    path('analysis/', include('analysis.urls')),
    path('generic-expenses/', include('general_expenses.urls')),
    path('notebook/', include('notebook.urls')),


    # tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # api
    path('api/', include('frontend.api.urls')),
    path('api/vendors/', include('vendors.api.urls')),


    # backups
    path("backup/taxes-modifier/", backup_taxes_view),

    path("backup/invoice-items/", backup_invoice_items_view),
    path("backup/my-cards/", backup_my_card_view),
    path("backup/customers/", backup_customers_view),
    path("backup/customers-details/", backup_customers_details_view),
    path("backup/payment-invoices/", backup_payments_invoices_view),

    path("backup/folder/general-expenses/", backup_general_expenses_folder_view),
    path("backup/folder/general-expenses-category/", backup_general_expenses_category_folder_view),

    path('backup/incomes/', backup_incomes_view),

    path('backup/tags/', backup_tags_view),
    path('backup/notebooks/', backup_notebook_view),

    path('backup/orders/', backup_orders_view),
    path('backup/orders/payment/', backup_orders_payment_view),

    path('backup/payments-methods/', backup_payment_methods_view),

    path('backup/generic-expenses/', backup_generic_expenses_view),
    path('backup/payrolls/', backup_payrolls_view),
    path('backup/occupation/', backup_occupation_view),
    path('backup/bills/', backup_bill_view),
    path('backup/bill-categories/', backup_bill_categories_view),
    path('backup/generic-expenses-category/', backup_generic_expenses_category_view),
    path('backup/persons/', backup_persons_view),

    path('backup/products/', backup_products_view),
    path('backup/products-vendor/', backup_products_vendor_view),
    path('backup/product-categories/', backup_categories_view),

    path('backup/vendors/', backup_vendors_view),
    path('backup/vendors-notes/', backup_vendor_notes_view),
    path('backup/employers/', backup_vendor_employers_view),
    path('backup/vendor-payments/', backup_vendor_payments_view),
    path('backup/vendor-banking-account/', backup_vendor_banking_account_view),
    path('backup/invoices/', backup_invoices_view),




]
