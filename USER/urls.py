
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
    path("category/<slug:category_slug>/", views.products_by_category, name="products_by_category"),
]
