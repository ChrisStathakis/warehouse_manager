from rest_framework import serializers

from ..models import Vendor, Payment, Paycheck, Invoice


class VendorSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_vendors:detail')

    class Meta:
        model = Vendor
        fields = ['active', 'job_description', 'title', 'owner', 'afm', 'doy', 'phone', 'cellphone',
                  'email', 'site', 'balance', 'paid_value', 'value', 'id', 'url'
                  ]


class VendorDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = ['active', 'job_description', 'title', 'owner', 'afm', 'doy', 'phone', 'cellphone',
                  'email', 'site', 'balance', 'paid_value', 'value', 'id'
                  ]


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['date', 'title', 'payment_method', 'vendor', 'value', 'description', 'tag_vendor', 'id']


class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = ['date', 'id', 'vendor', 'tag_vendor', 'vendor', 'value', 'extra_value', 'final_value'
                  , 'title'
                  ]



