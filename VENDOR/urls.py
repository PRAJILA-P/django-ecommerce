from django.urls import path, re_path
from . import views

app_name = "vendor"

urlpatterns = [
    # re_path(r'^$', views.index, name='index'),
    path('vendor_home/',views.vendor_home,name='vendor_home'),
    path('vendor/',views.vendor,name='vendor'),
    path('vendor/register/',views.register_vendor,name='vendor_register'),  
    path('vendor/login/', views.vendor_login, name='vendor_login'),
    path('vendor_profile/',views.vendor_profile,name='vendor_profile'),
    path('vendor/edit/<int:vendor_id>/', views.edit_vendor, name='edit_vendor'),
    path('logout/', views.vendor_logout, name='vendor_logout'),
    path('product_add/',views.addproduct,name='addproduct'),
    # path("products/", views.product_list, name="product_list"),
    # path('<slug:c_slug>/',views.allProdCat,name='products_by_category'),
    # path('vendor/home1/', views.vendor_home1, name='vendor_home1'),
    path("forgot-password/", views.forgot_password, name="vendor_forgot_password"),
    path("reset-password/<str:token>/", views.reset_password, name="reset_password"),
    # path("product_view/",views.product_view,name="product_view"),
    path('<slug:c_slug>/<slug:product_slug>/',views.proDetail,name='prodCatdetail'),
    path("product/<int:product_id>/edit/", views.edit_product, name="edit_product"),
    path("product/<int:product_id>/delete/", views.delete_product, name="delete_product"),
    path("products/",views.product_search_vendor,name="vendor_products"),

]
