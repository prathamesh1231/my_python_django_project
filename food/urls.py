from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('',            views.home,         name='home'),
    path('about/',      views.about,        name='about'),
    path('menu/',       views.menu_view,    name='menu'),
    path('contact/',    views.contact,      name='contact'),
    path('map/',        views.map_view,     name='map'),
    # Auth
    path('login/',      views.login_view,   name='login'),
    path('register/',   views.register_view,name='register'),
    path('logout/',     views.logout_view,  name='logout'),
    # Cart
    path('cart/',                       views.cart_view,      name='cart'),
    path('cart/add/<int:item_id>/',    views.add_to_cart,    name='add_to_cart'),
    path('cart/remove/<int:item_id>/',  views.remove_from_cart,name='remove_from_cart'),
    path('cart/update/<int:item_id>/',  views.update_cart,    name='update_cart'),
    # Orders
    path('checkout/',                   views.checkout,       name='checkout'),
    path('orders/',                     views.my_orders,      name='my_orders'),
    path('orders/<int:order_id>/',      views.order_detail,   name='order_detail'),
]
