from django.urls import include, path

from . import views

app_name = "orders"

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path('accounts/', include('django.contrib.auth.urls')),
    path("additem/", views.additem, name="additem"),
    path("cart/", views.cart, name="shoppin cart"),
    path("cart/removeitem/", views.removeitem, name="removeitem"),
    path("cart/placeorder/", views.placeorder, name="placeorder"),
    path("orders/", views.orders, name="orders"),
]
