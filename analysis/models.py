from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.


class TaxesModifier(models.Model):
    normal = models.IntegerField(default=80, verbose_name='24%')
    half = models.IntegerField(default=0, verbose_name='13%')
    six = models.IntegerField(default=20, verbose_name='6%')

    def __str__(self):
        return 'Taxes'

    def save(self, *args, **kwargs):
        if not self.pk and TaxesModifier.objects.exists():
            # if you'll not check for self.pk
            # then error will also raised in update of exists model
            raise ValidationError('There is can be only one Taxes instance')
        return super(TaxesModifier, self).save(*args, **kwargs)
