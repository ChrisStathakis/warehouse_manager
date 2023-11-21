from dal import autocomplete

from django import forms
from .models import Vendor, ProductVendor, Product, Category, PriceList
from orders.forms import BaseForm


class VendorForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(
        queryset=Vendor.objects.all(),
        widget=autocomplete.ModelSelect2(url='vendor-autocomplete')
    )

    class Meta:
        model = ProductVendor
        fields = ('__all__')


class ProductClassForm(BaseForm, forms.ModelForm):
    # vendors = forms.ModelChoiceField(queryset=Vendor.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Product
        fields = ['active', 'title', 'sku',  'categories',
                  'qty', 'value',
        ]


class ProductForm(BaseForm, forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=autocomplete.ModelSelect2(url='product-autocomplete')
    )

    class Meta:
        model = ProductVendor
        fields = ('__all__')


class ProductFrontEndForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Product
        fields = ['active', 'title', 'sku', 'categories',
                  'qty', 'value', 'value_per_unit', 'value_discount'
                ]
        

class ProductFrontEndAjaxForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Product
        fields = ['active', 'title', 'value', 'value_per_unit', 'value_discount'
                ]
        
    def __init__(self, *args, **kwargs):
        super(ProductFrontEndAjaxForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "New Email Label"
        self.fields['value'].label = "New Email Label"
        self.fields['value_per_unit'].label = "ΤΙΜΗ ΑΝΑ ΜΟΝΑΔΑ ΜΕΤΡΗΣΗΣ"
        self.fields['value_discount'].label = "ΕΚΠΤΩΤΙΚΗ ΤΙΜΗ"
        

class ProductVendorFrontEndform(BaseForm, forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = ProductVendor
        fields = ['is_favorite', 'product', 'vendor', 'sku', 'value', 'discount', 'added_value', 'taxes_modifier']
        widgets = {
            'vendor': autocomplete.ModelSelect2(url='vendor-autocomplete')
        }


class CategoryForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Category
        fields = ['active', 'name', 'parent']


class ActionVendorForm(BaseForm):
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.all(), label='Προμηθευτης', required=True)


class PriceListForm(BaseForm, forms.ModelForm):

    class Meta:
        model = PriceList
        fields = ['title', 'active']