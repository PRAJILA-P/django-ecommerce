
from django.urls import path,re_path

from . import views


app_name = "user"

urlpatterns = [

    re_path(r'^$', views.index, name='index'),
    path('user_register/',views.user_register,name='user_register'),
    path('user_login/',views.user_login,name='user_login'),
    path('user_profile/',views.user_profile,name='user_profile'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('user_edit_profile/<int:user_id>/',views.user_edit_profile,name='user_edit_profile'),

    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.order_list, name="order_list"),
    # path("orders/<int:order_id>/", views.order_list, name="order_list"),
    path("orders/<int:order_id>/",views.order_detail, name="order_detail"),

    path("cancel-order/<int:item_id>/", views.cancel_order_item, name="cancel_order_item"),
    path("cancel-whole-order/<int:order_id>/", views.cancel_order, name="cancel_order"),


    path("high-discount/<slug:category_slug>/", views.high_discount, name="high-discount"),
    path("high-price/<slug:category_slug>/", views.high_price, name="high-price"),
    path("low-price/<slug:category_slug>/", views.low_price, name="low-price"),



    path("category/<slug:category_slug>/", views.products_by_category, name="products_by_category"),
    path("<slug:category_slug>/<slug:product_slug>/", views.prodCatdetail, name="prodCatdetail"),

    path("cart/", views.view_cart, name="view_cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),

    path("cart/remove/<int:cart_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/update/<int:cart_id>/<str:action>/", views.update_quantity, name="update_quantity"),
     
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),


    path("search/", views.product_search, name="product_search"),

    
    # path("cancel-order/<int:order_id>/", views.cancel_order, name="cancel_order"),

    # path("orders/<int:order_id>/", views.order_detail, name="order_detail"),

   

]
