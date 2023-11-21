from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import permissions
from rest_framework.reverse import reverse

from .serializers import PaymentMethodSerializer
from ..models import PaymentMethod


@api_view(['GET', ])
@permission_classes((permissions.AllowAny, ))
def api_homepage_view(request, format=None):
    return Response({
        'vendors': reverse('api_vendors:home', request=request, format=format),
        'payments': reverse('api_payments', request=request, format=format)
    })


class PaymentMethodListApiView(ListAPIView):
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all()
