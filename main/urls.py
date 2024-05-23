from django.urls import path
from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('login', views.log_in, name='login'),
    path('logout', views.log_out, name='logout'),
    path('product/<int:id>', views.product_view, name='product'),
    path('add-to-cart', views.add_to_cart, name='add-to-cart'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('search', views.search, name='search'),
    path('dark', views.dark, name='dark'),
    path('font', views.font, name='font'),
]
