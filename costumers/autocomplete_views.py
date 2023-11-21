from dal import autocomplete
from .models import Product


class ProductAutocompleteView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Product.objects.none()
        qs = Product.filters_data(self.request, Product.objects.filter(active=True))
        return qs