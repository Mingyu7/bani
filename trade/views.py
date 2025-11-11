from django.views.generic import TemplateView

class ProductListView(TemplateView):
    template_name = 'trade/product_list.html'
