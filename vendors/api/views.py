from rest_framework import generics
from rest_framework import reverse
from rest_framework import filters
import django_filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.reverse import reverse

from .serializers import VendorSerializer, PaymentSerializer, InvoiceSerializer, VendorDetailSerializer
from ..models import Vendor, Payment, Invoice


@api_view(['GET', ])
@permission_classes((AllowAny, ))
def homepage_vendor_view(request, format=None):
    return Response({
        'vendors': reverse('api_vendors:list', request=request, format=format),
        'invoices': reverse('api_vendors:invoices', request=request, format=format),
        'payments': reverse('api_vendors:payments', request=request, format=format)
    }
    )


class VendorListApiView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['title', 'afm']


class VendorDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VendorDetailSerializer
    queryset = Vendor.objects.all()
    permission_classes = [IsAuthenticated, ]


class InvoiceListApiView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['vendor', 'payment_method', 'date']
    search_fields = ['title', ]


class InvoiceRetrieveUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated, ]


class PaymentListCreateApiView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, ]
    filterset_fields = ['vendor', 'payment_method']
