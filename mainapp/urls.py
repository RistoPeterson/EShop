from django.urls import path
from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('product/<slug>/', views.ProductDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('remove-single-item/<slug>/', views.remove_single_item, name='remove-single-item'),
    path('remove-from-cart/<slug:slug>/', views.remove_from_cart, name='remove-from-cart'),
    path('summary/', views.OrderSummary.as_view(), name='summary'),

]
