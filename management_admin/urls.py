
from django.urls import path,re_path

from . import views


app_name='ad_min'



urlpatterns = [
    path('', views.custom_admin_home, name="custom_admin_home"),
     path("login/", views.custom_admin_login, name="custom_admin_login"),
    path("dashboard/", views.custom_admin_dashboard, name="custom_admin_dashboard"),
    path("logout/", views.custom_admin_logout, name="custom_admin_logout"),
    
    path("user/view/",views.custom_admin_user,name="custom_admin_user"),
    path('user_edit/<int:user_id>/',views.custom_admin_user_edit,name="custom_admin_user_edit"),
    path("users/delete/<int:user_id>/", views.custom_admin_user_delete, name="custom_admin_user_delete"),

    path("user/product/<int:pk>/",views.custom_admin_product,name='custom_admin_product'),
    path("user/product/<int:pk>/delete/",views.custom_admin_product_delete,name='custom_admin_product_delete'),

    path("vendor/view/",views.custom_admin_vendor,name="custom_admin_vendor"),
    path('vendor/edit/<int:vendor_id>/', views.custom_admin_vendor_edit, name='custom_admin_vendor_edit'),
    path('vendor/delete/<int:vendor_id>/', views.custom_admin_vendor_delete, name='custom_admin_vendor_delete'),

    path("categories/", views.custom_admin_category_list, name="category_list"),
    path("categories/add/", views.custom_admin_category_add, name="category_add"),
    path("categories/edit/<int:pk>/", views.custom_admin_category_edit, name="category_edit"),
    path("categories/delete/<int:pk>/", views.custom_admin_category_delete, name="category_delete"),

    path('order/',views.custom_admin_order_list,name="custom_admin_order_list"),
    path('order/<int:order_id>/',views.custom_admin_order_detail,name="custom_admin_order_detail"),
    path("orders/<int:order_id>/delete/", views.custom_admin_order_delete, name="custom_admin_order_delete"),

    path("order-item/",views.custom_admin_order_item_list,name="custom_admin_order_item_list"),
    path("custom-admin/order-item/<int:pk>/edit/", views.custom_admin_order_item_detail, name="custom_admin_order_item_detail"),
    path("custom-admin/order-item/<int:pk>/delete/", views.custom_admin_order_item_delete, name="custom_admin_order_item_delete"),

    path('review/',views.custom_admin_review_list,name="custom_admin_review_list"),
    path('review/<int:review_id>/',views.custom_admin_review_detail,name="custom_admin_review_detail"),
    path('review/<int:review_id>/delete/',views.custom_admin_review_delete,name="custom_admin_review_delete"),


]
