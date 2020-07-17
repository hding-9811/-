from django.urls import path

from cart import views

urlpatterns = [
    path('option/', views.CartView.as_view(
        {"post": "add_cart", "get": "list_cart", "patch": "change_select", "delete": "delete_course","put":"change_expire"}))
]
