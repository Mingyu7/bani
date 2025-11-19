
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from .forms import ProductForm

class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    ordering = ['-created_at']
    paginate_by = 8
    template_name = 'trade/product_list.html'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'trade/product_detail.html'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'trade/product_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('trade:product_detail', kwargs={'pk': self.object.pk})

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'trade/product_form.html'

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.author

    def get_success_url(self):
        return reverse_lazy('trade:product_detail', kwargs={'pk': self.object.pk})

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'trade/product_confirm_delete.html'
    success_url = reverse_lazy('trade:product_list')

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.author


