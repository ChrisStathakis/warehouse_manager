from django import forms
from .models import Costumer, PaymentInvoice, CostumerDetails, InvoiceItem, Product
from dal import autocomplete


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CostumerForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Costumer
        fields = ['active', 'eponimia', 'cellphone', 'afm', 'doy',
                  'address', 'city', 'job_description', 'loading_place',
                  'destination_city', 'transport', 'phone', 'notes'
         ]


class PaymentInvoiceForm(BaseForm, forms.ModelForm):
    date = forms.DateTimeField(required=True, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),label='Ημερομηνια')

    class Meta:
        model = PaymentInvoice
        fields = ['date', "delivery_time", "place", "writing_qty", "number_of_invoice",
                  'order_type', 'series', 'card_info', 'costumer',

                  ]

    def clean_date(self):
        date = self.cleaned_data.get('date', '')
        return date


class PaymentInvoiceEditForm(PaymentInvoiceForm):
    series = forms.CharField(widget=forms.HiddenInput())
    order_type = forms.CharField(widget=forms.HiddenInput())
    costumer = forms.ModelChoiceField(queryset=Costumer.objects.all(), widget=forms.HiddenInput())


class CostumerDetailsForm(BaseForm, forms.ModelForm):
    costumer = forms.ModelChoiceField(queryset=Costumer.objects.all(), widget=forms.HiddenInput(), required=True)
    invoice = forms.ModelChoiceField(queryset=PaymentInvoice.objects.all(), widget=forms.HiddenInput(), required=True)

    class Meta:
        model = CostumerDetails
        fields = '__all__'


class CreateInvoiceItemForm(BaseForm, forms.ModelForm):
    invoice = forms.ModelChoiceField(queryset=PaymentInvoice.objects.all(), widget=forms.HiddenInput(), required=True)
    # product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput(), required=True)

    class Meta:
        model = InvoiceItem
        fields = ['title', 'unit', 'qty', "sell_price",
                  'taxes_modifier', 'invoice']


class UpdateInvoiceItemForm(BaseForm, forms.ModelForm):
    invoice = forms.ModelChoiceField(queryset=PaymentInvoice.objects.all(), widget=forms.HiddenInput(), required=True)
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput(), required=True)

    class Meta:
        model = InvoiceItem
        fields = ['title', 'product', 'unit', "sell_price", 'qty', 'invoice']


