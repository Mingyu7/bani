from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    create_trade_chat,
    toggle_wishlist,
)

app_name = 'trade'

urlpatterns = [

    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/new/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:product_pk>/wishlist/', toggle_wishlist, name='toggle_wishlist'),
    path('chat/<str:username>/', create_trade_chat, name='create_trade_chat'),

]
