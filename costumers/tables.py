import django_tables2 as tables

from .models import PaymentInvoice


class PaymentInvoiceTable(tables.Table):
    button = tables.TemplateColumn("<a href='{{ record.get_edit_url }}' "
    "{% if record.locked %} class='btn btn-info' {% else %} class='btn btn-danger' {% endif %} ><i class='fa fa-edit'></i></a>",
                                   orderable=False, verbose_name='Επιλογες'
                                   )
    my_str = tables.TemplateColumn('<p>{{ record.get_series_display }} {{ record.number }} </p>')

    tag_total_value = tables.Column(orderable=False, verbose_name='Τελικη Αξια')

    class Meta:
        model = PaymentInvoice
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'my_str', 'order_type', 'costumer', 'tag_total_value']

