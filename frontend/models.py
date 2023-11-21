from django.db import models

# Create your models here.

PAYMENT_METHOD_CATEGORY = (
    ('a', 'Αντικαταβολή'),
    ('b', 'Τραπεζική ΚατάΘεση')
)


class PaymentMethod(models.Model):
    title = models.CharField(max_length=200, unique=True)
    category = models.CharField(max_length=1, choices=PAYMENT_METHOD_CATEGORY)

    def __str__(self):
        return self.title
