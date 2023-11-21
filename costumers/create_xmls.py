from rest_framework import routers, serializers, viewsets
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer

from .models import PaymentInvoice


class InvoiceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PaymentInvoice
        fields = ['series', 'number']


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = PaymentInvoice.objects.all()
    serializer_class = InvoiceSerializer
    parser_classes = (XMLParser, )
    renderer_classes = (XMLRenderer)