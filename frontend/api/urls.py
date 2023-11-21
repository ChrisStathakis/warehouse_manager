from django.urls import path

from .views import api_homepage_view, PaymentMethodListApiView


urlpatterns = [
    path('', api_homepage_view),
    path('payment-methods/', PaymentMethodListApiView.as_view(), name='api_payments')
]