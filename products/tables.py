import django_tables2 as tables

from .models import Product, Category, ProductVendor, PriceList


class ProductVendorTable(tables.Table):
    action = tables.TemplateColumn('''
                                <div class="btn-group dropright">
                                            <button data-href='{% url 'vendors:ajax_product_modal_quick_view' record.product.id %}' class='btn btn-success quick_view'>
                                            <i class='fa fa-print'> </i> 
                                            </button>
                                            <button type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                <span class="sr-only">Toggle Dropright</span>
                                            </button>
                                                <div class="dropdown-menu">
                                                     <a target="_blank" class="dropdown-item" href="{% url 'edit_product_update' record.product.id %}" %}">Επεξεργασια</a>     
                                                </div>
                                            </div>
                                ''',
        orderable=False, verbose_name='Επεξεργασία'
    )
    tag_value = tables.Column(orderable=False, verbose_name='Καθαρη Αξια')
    tag_final_value = tables.Column(orderable=False, verbose_name='Αξια')

    vendor = tables.TemplateColumn("<p> {{ record.vendor|truncatechars:'20' }}</p>")

    class Meta:
        model = ProductVendor
        template_name = 'django_tables2/bootstrap.html'
        fields = ['id', 'product', 'sku', 'vendor', 'tag_clean_value', 'tag_final_value', 'action']


class ProductTable(tables.Table):
    """
    mycheck_box = tables.TemplateColumn('''
    <div class="form-check">
        <label class="form-check-label">
            <input class="form-check-input myCheck" type="checkbox" value="{{ record.id }}" name="choose_product">
            <span class="form-check-sign">
                <span class="check"></span>
            </span>
         </label>
    </div>
    ''', orderable=False, verbose_name='Επιλογη')
    """

    action = tables.TemplateColumn(
        '''<div class="btn-group dropright">
              <a href="{{ record.get_edit_url }}" class="btn btn-primary ">
               <i class='fa fa-edit'></i>
              </a>
              <button type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <span class="sr-only">Toggle Dropright</span>
              </button>
              <div class="dropdown-menu">
                <a class="dropdown-item" href="{{ record.get_edit_url }}" target="_blank">Ανοιγμα σε νεο παραθυρο</a>
                <a class="dropdown-item" href="{{ record.get_copy_url }}" target="_blank">Αντιγραφή Προϊόντων</a>
              </div>
            </div>''',
        orderable=False, verbose_name='Επεξεργασία'
    )
    tag_final_value = tables.Column(orderable=False, verbose_name='Τιμή Πώλησης')
    tag_price_buy = tables.Column(orderable=False, verbose_name='Τιμή Αγοράς')
    tag_average_price = tables.Column(orderable=False, verbose_name='Μεση Τιμή Αγοράς')
    qty = tables.TemplateColumn("<p style='background-color:{{ record.tag_color_qty}}'>{{ record.qty }} </p>", orderable=False)
    class Meta:
        model = Product
        template_name = 'django_tables2/bootstrap.html'
        fields = ['id', 'sku', 'title', 'qty', 'tag_final_value', 'tag_price_buy', 'tag_average_price']


class ProductTableForCategory(tables.Table):
    quick_view = tables.TemplateColumn(
        "<a data-href='{% url 'vendors:ajax_product_analysis' record.id %}' class='btn btn-primary btn-round"
        " quick-view'><i class='fa fa-eye'></i></a>",
        orderable=False, verbose_name='Αναλυση'
    )
    tag_price_buy = tables.Column(verbose_name='Χαμηλοτερη τιμη', orderable=False)
    tag_vendors = tables.Column(verbose_name='VENDORS', orderable=False)
    tag_final_value = tables.Column(verbose_name='Αξια', orderable=False)
    title = tables.TemplateColumn("<a target='_blank' style='text-decoration: none;color:black' href='{{ record.get_edit_url }}'>"
                                  "{{ record }} </a>")
    delete = tables.TemplateColumn("<button data-href='{% url 'vendors:ajax_manipulate_product_category' category.id record.id 'delete' %}' "
                                   "class='btn btn-danger delete_class'><i class='fa fa-trash'></i></button>", verbose_name="ΔΙΑΓΡΑΦΗ")

    class Meta:
        model = Product
        template_name = 'django_tables2/bootstrap.html'
        fields = ['delete', 'title', 'tag_price_buy', 'tag_final_value', "margin", "tag_vendors", 'quick_view', ]


class ProductCategoriesTable(tables.Table):
    quick_view = tables.TemplateColumn(
        "<a data-href='{{ record.get_modal_url }}' class='btn btn-success btn-round'><i class='fa fa-eye'></i></a>",
        orderable=False, verbose_name='Επεξεργασία'
    )


class CategoryTable(tables.Table):
    card = tables.TemplateColumn(
        "<a href='{{ record.get_card_url }}' class='btn btn-success btn-round'><i class='fa fa-eye'></i></a>",
        orderable=False,
    )
    action = tables.TemplateColumn(
        "<a href='{{ record.get_edit_url }}' class='btn btn-primary btn-round'><i class='fa fa-edit'></i></a>",
        orderable=False,
    )

    class Meta:
        model = Category
        template_name = 'django_tables2/bootstrap.html'
        fields = ['name', 'parent', 'active' ]


class PriceTable(tables.Table):
    action = tables.TemplateColumn(
        "<a href='{{ record.get_absolute_url }}' class='btn btn-primary btn-round'><i class='fa fa-edit'></i></a>",
        orderable=False,
    )

    class Meta:
        model = PriceList
        template_name = 'django_tables2/bootstrap.html'
        fields = ['title', 'active']

