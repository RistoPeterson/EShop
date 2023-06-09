from django.urls import path
from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.HomeView, name='index'),
    path('all-products', views.IndexView.as_view(), name='all_products'),
    path('popular-products', views.PopView.as_view(), name='popular_items'),
    path('new-arrivals', views.NewArrivals.as_view(), name='new_arrivals'),
    path('product/<slug>/', views.ProductDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('remove-single-item/<slug>/', views.remove_single_item, name='remove-single-item'),
    path('remove-from-cart/<slug:slug>/', views.remove_from_cart, name='remove-from-cart'),
    path('summary/', views.OrderSummary.as_view(), name='summary'),
    path('shipping-address/', views.ShippingAddressView.as_view(), name='shipping'),
    path('about/', views.About, name='about'),
    path('add-coupon/', views.addCouponView.as_view(), name='add-coupon'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('profile/', views.Profile, name='profile'),

]
