from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProductListAPTView.as_view(), name="product_list"),

]