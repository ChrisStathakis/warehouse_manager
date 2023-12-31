from django.urls import path
from .views import (HomepageView, VendorListView, CreateVendorView, UpdateVendorView, delete_vendor_view,
                    VendorNotesView, delete_note_view, NoteUpdateView, VendorCardView, change_note_status_view,
                    create_costumer_from_vendor_view, PaycheckUpdateView, PaycheckListView, 
                    paycheck_delete_view, paycheck_create_view, print_vendor_view, invoices_vendor_list_view,
                    CreateInvoiceView, InvoiceDetailView, InvoiceListView
                    )

from .action_views import (validate_invoice_form_view, validate_employer_view, validate_order_item_update_view,
                           validate_payment_form_view, validate_invoice_edit_form_view, delete_invoice_view, 
                           delete_payment_view, validate_payment_edit_form_view, validate_employer_edit_view,
                           delete_employer_view, validate_create_banking_account_view, delete_invoice_item_view,
                           validate_edit_banking_account_view, delete_banking_account_view, validate_note_creation_view,
                           validate_product_creation_view, validate_product_edit_view, validate_product_vendor_edit_view,
                           copy_product_to_new_vendor, copy_product_from_vendor_card_view, action_favorite_view,
                           action_form_copy_vendor_product_view, validate_paycheck_form_view, validate_create_invoice_order_item_view,
                           create_product_from_invoice

                           
               )
from .ajax_views import (ajax_invoice_modal_view, ajax_invoice_modal_view, 
                         ajax_employer_edit_modal_view, ajax_banking_account_create_modal_view, ajax_banking_account_edit_modal_view, 
                         ajax_payment_edit_modal_view, ajax_show_product_prices, ajax_calculate_vendors_balance_view, ajax_search_warehouse_view,
                         ajax_edit_product_modal, ajax_product_modal_quick_view, ajax_show_product_analysis_view,
                         ajax_search_products, ajax_add_product_to_category_view, ajax_edit_product_submit_view, create_product_from_category_view,
                         ajax_search_products_warehouse_view, ajax_modify_order_item_modal, ajax_create_product_modal
                         )

from .categories_views import (CategoryListView, CategoryUpdateView, category_delete_view, CategoryCreateView,
                               CategoryCardListView, print_category_products_view
                               )
app_name = 'vendors'


urlpatterns = [
    path('home/', HomepageView.as_view(), name='home'),
    path('list/', VendorListView.as_view(), name='list'),
    path('create/', CreateVendorView.as_view(), name='create'),
    path('update/<int:pk>/', UpdateVendorView.as_view(), name='update'),
    path('delelte/vendor/<int:pk>/', delete_vendor_view, name='delete'),

    # invoices
    path("invoices/list/", InvoiceListView.as_view(), name="invoice_list"),
    path("invoices/vendor/<int:pk>/", invoices_vendor_list_view, name="invoices_vendor"),
    path("invoices/create/<int:pk>/", CreateInvoiceView.as_view(), name="invoice_vendor_create"),
    path('invoice-detail/<int:pk>/', InvoiceDetailView.as_view(), name='invoice_update'),
    path('invoice-delete-<int:pk>/', delete_invoice_view, name='invoice_delete'),
    path('validate-order-item-creation/<int:pk>/', validate_order_item_update_view, name='validate_order_item_update'),
    path('delete-invoice-item/<int:pk>/', delete_invoice_item_view, name='delete_invoice_item'),

    path('validate-order-item_creation/<int:pk>/', validate_create_invoice_order_item_view, name='validate_order_item_creation'),

    path('create-costumer-from-vendor/<int:pk>/', create_costumer_from_vendor_view, name='create_costumer_from_vendor'),
    path('kartela/<int:pk>/', VendorCardView.as_view(), name='vendor_card'),
    path('ajax/kartela/product/<int:pk>/', ajax_show_product_prices, name='ajax_product_price'),
    path('ajax/calculate-vendors-balance/', ajax_calculate_vendors_balance_view, name='ajax_vendors_balance'),
    path('ajax-search-warehouse/<int:pk>/', ajax_search_warehouse_view, name='ajax_search_warehouse'),
    path('ajax/edit-product/<int:pk>/', ajax_edit_product_modal, name='ajax_edit_product'),
    path('action/validate/product-edit/<int:pk>/', validate_product_edit_view, name='validate_product_edit'),
    path('action/validate/product-vendor/<int:pk>/', validate_product_vendor_edit_view, name='validate_product_vendor_edit'),
    path('action/favorite-product/<int:pk>/', action_favorite_view, name='action_favorite_product'), 
    path('ajax/product-modal/quick-view/<int:pk>/', ajax_product_modal_quick_view, name='ajax_product_modal_quick_view'),
    path('copy-product-for=new-vendor/<int:pk>/', copy_product_to_new_vendor, name='copy_product_for_new_vendor'),
    path('copy-product-from-vendor/<int:pk>/<int:dk>/', copy_product_from_vendor_card_view, name='copy_product_from_vendor'),

    path('paycheck/list/', PaycheckListView.as_view(), name='paycheck_list'),
    path('paycheck/create/', paycheck_create_view, name='paycheck_create'),
    path('paycheck/detail/<int:pk>/', PaycheckUpdateView.as_view(), name='paycheck_update'),
    path('paychech/delete/<int:pk>/', paycheck_delete_view, name='paycheck_delete'),
    path('print/vendor/<int:pk>/', print_vendor_view, name='print_vendor_view'),

    #  notes
    path('notes/<int:pk>/', VendorNotesView.as_view(), name='notes'),
    path('notes/validate-creation/<int:pk>/', validate_note_creation_view, name='note_create'),
    path('notes/update/<int:pk>/', NoteUpdateView.as_view(), name='note_update'),
    path('notes/status-update/<int:pk>/', change_note_status_view, name='note_update_status'),
    path('notes/delete/<int:pk>/', delete_note_view, name='note_delete'),
    
    path('actions/validate-invoice-form/<int:pk>/', validate_invoice_form_view, name='validate_invoice_view'),
    path('actions/validate-payment-form/<int:pk>/', validate_payment_form_view, name='validate_payment_view'),
    path('actions/validate-employer-form/<int:pk>/', validate_employer_view, name='validate_employer_view'),
    path('actions/validate-product-creation-view/<int:pk>/', validate_product_creation_view, name='validate_product_creation'),
    path('actions/copy/product-from-vendor-card/<int:pk>/', action_form_copy_vendor_product_view, name='action_copy_product_vendor'),

    path('ajax/invoice-modal/<int:pk>/', ajax_invoice_modal_view, name='ajax_invoice_modal'),
    path('actions/validate-invoice-edit-form/<int:pk>/', validate_invoice_edit_form_view, name='validate_invoice_edit_view'),
    path('actions/invoice-delete/<int:pk>/', delete_invoice_view, name='action_delete_invoice'),

    path('ajax/payment-modal/<int:pk>/', ajax_payment_edit_modal_view, name='ajax_payment_modal'),
    path('actions/validate-payment-edit-form/<int:pk>/', validate_payment_edit_form_view, name='validate_payment_edit_view'),
    path('actions/payment-delete/<int:pk>/', delete_payment_view, name='action_delete_payment'),
    path('actions/paycheck/validate-create/<int:pk>/', validate_paycheck_form_view, name='validate_paycheck_create' ),

    #  employer links
    path('actions/validate-employer-edit-form/<int:pk>/', validate_employer_edit_view, name='validate_employer_edit_view'),
    path('actions/employer-delete/<int:pk>/', delete_employer_view, name='action_delete_employer'),
    path('ajax/employer-modal/<int:pk>/', ajax_employer_edit_modal_view, name='ajax_employer_modal'),

    # banking accounts
    path('ajax/modal/banking-account/<int:pk>/', ajax_banking_account_create_modal_view, name='ajax_create_banking_account'),
    path('ajax/modal/banking-account-edit/<int:pk>/', ajax_banking_account_edit_modal_view, name='ajax_edit_banking_account'),
    path('validate/banking-account-create/<int:pk>/', validate_create_banking_account_view, name='validate_create_banking_account'),
    path('validate/banking_account-edit/<int:pk>/', validate_edit_banking_account_view, name='validate_edit_banking_account'),
    path('banking-account-delete/<int:pk>/', delete_banking_account_view, name='delete_account_banking_view'),

    # categories
    path('categories-list/', CategoryListView.as_view(), name='category_list'),
    path('categories-update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/delete/<int:pk>/', category_delete_view, name='category_delete'),
    path('category/card-view/<int:pk>/', CategoryCardListView.as_view(), name='category_card'),
    path('ajax/category/product-analysis/<int:pk>/', ajax_show_product_analysis_view, name='ajax_product_analysis'),
    path('print/category/<int:pk>/', print_category_products_view, name="print_category"),


    # actions

    path("ajax/manipulate-product-category/<int:pk>/<int:dk>/<str:action>/", ajax_add_product_to_category_view,
         name="ajax_manipulate_product_category"),
    path("ajax/edit-product-submit/<int:pk>/<int:dk>/", ajax_edit_product_submit_view, name="edit_product_submit"),
    path("ajax/search-products/<int:pk>/", ajax_search_products, name="products_ajax_search"),
    path("submit/create-products-from-category/<int:pk>/", create_product_from_category_view,
         name="create_product_from_category_view"),

    path('action-create-product-from-invoice/<int:pk>/', create_product_from_invoice, name='create_product_from_invoice'),     

    # ajax
    path('ajax-create-product-from-invoice/<int:pk>/<int:dk>/', ajax_create_product_modal, name='ajax_create_product'),
    path('ajax-modify-order-item-modal/<int:pk>/', ajax_modify_order_item_modal, name='ajax_modify_order_item'),
    path('ware-search-products/<int:pk>/', ajax_search_products_warehouse_view, name='search_products_ware'),



    ]
