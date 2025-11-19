
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from .forms import ProductForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 8
    template_name = 'trade/product_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at') # Default sort
        
        # Search
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        # Sort
        sort_by = self.request.GET.get('sort', 'latest')
        if sort_by == 'oldest':
            queryset = queryset.order_by('created_at')
        else: # 'latest' or default
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['sort_by'] = self.request.GET.get('sort', 'latest')
        return context

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

@login_required
def create_trade_chat(request, username):
    other_user = User.objects.get(username=username)
    
    # Create a unique room name for the two users
    if request.user.id > other_user.id:
        room_name = f'trade_{request.user.id}-{other_user.id}'
    else:
        room_name = f'trade_{other_user.id}-{request.user.id}'

    # Redirect to the chat room
    return redirect('message:room', room_name=room_name)


