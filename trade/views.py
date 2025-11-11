from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class ProductListView(TemplateView):
    template_name = 'trade/product_list.html'

class ProductCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'trade/product_form.html'
