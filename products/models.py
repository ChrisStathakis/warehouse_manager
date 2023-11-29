from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from vendors.models import Vendor, TAXES_CHOICES
from django.db.models import Min, Q, Avg, Sum, Window, F

from frontend.my_constants import UNITS

PRODUCTION = settings.PRODUCTION
CURRENCY = settings.CURRENCY


class PriceList(models.Model):
    active = models.BooleanField(default=False)
    title = models.CharField(max_length=220)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('price_list_update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse("price_list_delete", kwargs={"pk": self.id})

    @staticmethod
    def get_create_url():
        return reverse("price_list_create")


class Category(models.Model):
    name = models.CharField(max_length=240, unique=True)

    
    def __str__(self):
        return self.name

    def get_edit_url(self):
        return reverse('vendors:category_update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('vendors:category_delete', kwargs={'pk': self.id})

    def get_card_url(self):
        return reverse('vendors:category_card', kwargs={'pk': self.id})

    @staticmethod
    def filters_data(request, qs):
        search_name = request.GET.get('search_name', None)
        q = request.GET.get('q', None)
        qs = qs.filter(name__icontains=q) if q else qs
        qs = qs.filter(name__contains=search_name) if search_name else qs
        return qs

    
class Product(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=150, verbose_name='Ονομασια')
    sku = models.CharField(max_length=50, blank=True)
    order_code = models.CharField(max_length=220, blank=True, null=True)
    barcode = models.CharField(max_length=20, blank=True)
    vendors = models.ManyToManyField(Vendor, through='ProductVendor', verbose_name='Προμηθευτές', blank=True)
    unit = models.CharField(default='a', max_length=1, choices=UNITS)
    categories = models.ManyToManyField(Category, verbose_name='Κατηγορίες', blank=True)
    qty = models.DecimalField(default=0, verbose_name='Ποσότητα', decimal_places=2, max_digits=20)
    safe_qty = models.IntegerField(default=0, null=True, verbose_name="Ελάχιστη ποσότητα")
    price_buy = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Τελευταία Τιμή Αγοράς', default=0.00)
    value = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Τιμή Πώλησης', )

    average_price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Μεση Τιμή', default=0.00)
    running_average_price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Τρέχων Μεση Τιμή', default=0.00)

    final_value = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    margin = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    taxes_modifier = models.CharField(max_length=1, choices=TAXES_CHOICES, null=True, blank=True)
    price_list = models.ManyToManyField(PriceList, verbose_name="prices_list", blank=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Προϊόν'
         # verbose_plural_name = 'Προϊόντα'

    
    def save(self, *args, **kwargs):
        self.title = self.title.upper()
        self.barcode = self.create_barcode()
        self.final_value = self.value

        invoice_qs = self.invoice_vendor_items.all()
        self.running_average_price = invoice_qs[:3].aggregate(avg=Avg("value"))['avg'] or 0
        sell_qs = self.sell_items.all()
        add_qty = invoice_qs.aggregate(total_qty=Sum("qty"))['total_qty'] if invoice_qs.exists() else 0
        sell_qty = sell_qs.aggregate(total_qty=Sum("qty"))["total_qty"] if sell_qs.exists() else 0

        self.qty = add_qty - sell_qty
        self.margin = 0
        self.average_price = self.estimate_average_price(invoice_qs)
        if invoice_qs:
            self.price_buy = invoice_qs.first().value
        else:
            self.price_buy = 0
        super(Product, self).save(*args, **kwargs)

    def estimate_average_price(self, invoice_qs):
        remaining_qty = invoice_qs.aggregate(total_qty=Sum("remaining_qty"))['total_qty'] if invoice_qs.exists() else 0
        remaining_total_cost = invoice_qs.aggregate(total=Sum("remaining_total_cost"))['total'] if invoice_qs.exists() else 0
        print(remaining_qty, remaining_total_cost)
        return remaining_total_cost/remaining_qty if remaining_qty != 0 else 0
    
    def get_edit_url(self):
        return reverse('edit_product_update', kwargs={'pk': self.id})

    def get_copy_url(self):
        return reverse('copy_product_view', kwargs={'pk': self.id})

    def tag_color_qty(self):
        if self.safe_qty == 0:
            return 'white'
        if self.qty - self.safe_qty > 2:
            return 'red'
        return 'white'

    def tag_average_price(self):
        return f'{self.average_price} {CURRENCY}'

    def tag_final_value(self):
        final_value = round(self.final_value, 2)
        return f'{final_value} {CURRENCY}'
    tag_final_value.short_description = 'Αξια'

    def tag_price_buy(self):
        return f'{round(self.price_buy, 2)} {CURRENCY}'

    def __str__(self):
        return self.title

    def find_value(self):
        items = self.product_vendors.all()
        price = items.aggregate(Min('final_value'))['final_value__min'] if items.exists() else 0.00
        apography_price = items.aggregate(Avg('clean_value'))['clean_value__avg'] if items.exists() else 0.00
        self.price_buy = price
        self.apography = apography_price
        self.save()

    def create_barcode(self):
        try:
            id = str(self.id)
            total_zeros = 10- len(id)
            return '0'*total_zeros + id
        except:
            return ''

    def tag_vendors(self):
        my_string = ''
        ddd = ProductVendor.objects.filter(product=self)
        for dd in ddd:
            my_string += f'{dd.vendor} --> {dd.final_value} {CURRENCY} | '
        return my_string

    @staticmethod
    def filters_data(request, qs):
        search_name = request.GET.get('search_name', None)
        check_vendor = request.GET.get('check_vendor_name', None)
        q = request.GET.get('q', None)
        vendor_name = request.GET.getlist('vendor_name', None)
        cate_name = request.GET.getlist('cate_name', None)
        qs = qs.filter(vendors__in=vendor_name) if vendor_name else qs
        qs = qs.filter(vendors__isnull=True) if check_vendor == 'have_' else qs
        if PRODUCTION:
            if q:
                #qa = qa.SearchQuery(q)
                qs = qs.filter(Q(title__search=q) |
                               Q(sku__search=q) |
                               Q(title__icontains=q)
                               ).distinct()
                # qs = qs.annotate(search=SearchVector('title', config='greece'),).filter(search=SearchQuery(q, config='greece'))
                # qs = qs.annotate(similarity=TrigramSimilarity('title', q),).filter(similarity__gt=0.3).order_by('-similarity')
            if search_name:
                qs = qs.filter(Q(title__search=search_name) |
                               Q(title__icontains=search_name) |
                               Q(sku__icontains=search_name)
                               ).distinct()
        else:
            if q:
                qs = qs.filter(title__icontains=q.upper())
            if search_name:
                qs = qs.filter(title__icontains=search_name.upper())


        return qs


class ProductVendor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Προϊον', related_name='product_vendors')
    is_favorite = models.BooleanField(default=False, verbose_name='Αγαπημένο')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name='Προμηθευτης', blank=True)
    sku = models.CharField(max_length=150, verbose_name='Κωδικος Τιμολογιου', blank=True)
    value = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Αρχική Αξία')
    discount = models.IntegerField(default=0, verbose_name='Εκπτωση')
    clean_value = models.DecimalField(default=0, decimal_places=2, max_digits=10, verbose_name='Καθαρη Αξια')
    taxes_value = models.DecimalField(default=0, decimal_places=2, max_digits=10, verbose_name='Αξια μετα Φορους')
    added_value = models.DecimalField(default=0, decimal_places=2, max_digits=10, verbose_name='Επιπλεον Αξια')
    
    final_value = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, verbose_name='Τελικη Αξια')
    taxes_modifier = models.CharField(max_length=1, choices=TAXES_CHOICES, default='c')

    class Meta:
        ordering = ['-is_favorite', 'product__title']

    def save(self, *args, **kwargs):
        taxes = self.get_taxes_modifier_display()+100
        self.clean_value = self.value * (100-int(self.discount))/100
        self.taxes_value = self.clean_value * (taxes)/100
        self.final_value = self.taxes_value + self.added_value
        super().save(*args, **kwargs)
        self.product.find_value()

    def __str__(self):
        return f'{self.product} | {self.vendor}'

    def tag_final_value(self):
        return f'{self.final_value} {CURRENCY}'
    tag_final_value.short_description = 'Αξια'

    def tag_discount(self):
        return f'{self.discount} %'

    def tag_value(self):
        return f'{self.value} {CURRENCY}'

    def tag_clean_value(self):
        return f'{self.clean_value} {CURRENCY}'

    def tag_taxes_value(self):
        return f'{self.taxes_value} {CURRENCY}'

    def tag_added_value(self):
        return f'{self.added_value} {CURRENCY}'

    def get_edit_url(self):
        return reverse('product_vendor_edit', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('product_vendor_delete', kwargs={'pk': self.id})

    @staticmethod
    def filters_data(request, qs):
        search_name = request.GET.get('search_name', None)
        fav_name = request.GET.get('fav_name', None)
        q = request.GET.get('q', None)
        cate_name = request.GET.getlist('cate_name', None)
        vendor_name = request.GET.getlist('vendor_name', None)
        qs = qs.filter(is_favorite=True) if fav_name == 'have_' else qs
        if cate_name:
            products = qs.values_list('product')
            pro_qs = Product.objects.filter(id__in=products, categories__in=cate_name)
            qs = qs.filter(product__in=pro_qs)
        
        qs = qs.filter(vendor__id__in=vendor_name) if vendor_name else qs

        if search_name:
            qs = qs.filter(Q(product__title__icontains=search_name) |
                           Q(sku__icontains=search_name) |
                           Q(vendor__title__icontains=search_name)
                        ).distinct()
        if q:
            qs = qs.filter(Q(product__title__icontains=q) |
                           Q(sku__icontains=q) |
                           Q(vendor__title__icontains=q)
                        ).distinct()
        return qs

