from .autocomplete_view import VendorAutocomplete, CategoryAutocomplete, ProductAutoComplete
from django.urls import path, re_path
from .views import (ProductHomepageView, ProductListView, ProductEditListView, ProductCreateView, ProductUpdateView,
                    create_product_vendor_view, product_vendor_delete_view, ProductVendorUpdateView, delete_product_view, copy_product_view,
                    update_product_fpa_view, manipulate_apografi_view,
                    PriceListCreateView, PriceListUpdateView, PriceListView, delete_price_list_view, print_price_list_view

                    )

from .action_views import action_choose_vendor_view
from .product_vendors import ProductVendorListView
from .data_views import fix_products_titles_view
from .ajax_views import ajax_add_product_to_price_list_view, ajax_edit_product_submit_view, ajax_search_products, create_product_from_price_time_view

urlpatterns = [
    path('apografi/', manipulate_apografi_view),
    path('fpa/', update_product_fpa_view),
    path('homepage/', ProductHomepageView.as_view(), name='product_homepage'), 
    path('list-analysis/', ProductListView.as_view(), name='product_list_analysis'),


    path('edit-views/product/list/', ProductEditListView.as_view(), name='edit_product_list'),
    path('edit-views/product/create/', ProductCreateView.as_view(), name='edit_product_create'),
    path('edit-views/product/update/<int:pk>/', ProductUpdateView.as_view(), name='edit_product_update'),
    path('edit-views/product-vendor-create/<int:pk>/', create_product_vendor_view, name='product_vendor_create'),
    path('edit-views/product-delete/<int:pk>/', delete_product_view, name='edit_product_delete'),

    path('edit-views/product-vendor/<int:pk>/', ProductVendorUpdateView.as_view(), name='product_vendor_edit'),
    path('edit-views/product-vendor-delete/<int:pk>/', product_vendor_delete_view, name='product_vendor_delete'),
    path('edit-views/product/copy/<int:pk>/', copy_product_view, name='copy_product_view'),


    # price lists
    path('price-lists/', PriceListView.as_view(), name="price_list_view"),
    path('price-lists/create/', PriceListCreateView.as_view(), name="price_list_create"),
    path('price-lists/update/<int:pk>/',  PriceListUpdateView.as_view(), name="price_list_update"),
    path('price-lists/delete/<int:pk>/', delete_price_list_view, name="price_list_delete"),


    re_path(r'^vendor-autocomplete/$', VendorAutocomplete.as_view(), name='vendor-autocomplete', ),
    re_path(r'^category-autocomplete/$', CategoryAutocomplete.as_view(), name='category-autocomplete', ),
    re_path(r'^product-autocomplete/$', ProductAutoComplete.as_view(), name='product-autocomplete', ),

    # products vendors
    path('product-vendors/list/', ProductVendorListView.as_view(), name='products_vendors_list'),

    # actions
    path('action/choose-vendor/', action_choose_vendor_view, name='action_choose_vendor'),
    path("ajax/manipulate-product-category/<int:pk>/<int:dk>/<str:action>/", ajax_add_product_to_price_list_view,
         name="ajax_manipulate_product_category"),
    path("ajax/edit-product-submit/<int:pk>/<int:dk>/", ajax_edit_product_submit_view, name="edit_product_submit"),
    path("ajax/search-products/<int:pk>/", ajax_search_products, name="products_ajax_search"),
    path("submit/create-products-from-price-list/<int:pk>/", create_product_from_price_time_view,
         name="create_product_from_price_time_view"),

    path("print/price-list/<int:pk>/", print_price_list_view, name="price_list_print"),

    # backups
    path('fix-titles/', fix_products_titles_view)
]
