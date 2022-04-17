from core import views
#from core import models
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
     
#Restaurant
    path('', views.index, name='index'),

# Account
    path('register/', views.register, name="signup"),
    path('profile/', views.profile, name="profile"),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.user_password, name='user_password'),

    path("login/", auth_views.LoginView.as_view(template_name='accounts/login.html',
         redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'), name="logout"),
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html'), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'), name="password_reset_complete"),

#Category and Items
    path("ItemCategory",views.ItemCategory, name="ItemCategory"),

#Cart and Order
    path("cart",views.add_to_cart,name="cart"),
    path("get_cart_data",views.get_cart_data,name="get_cart_data"),
    path("change_quan",views.change_quan,name="change_quan"),

#Checkout and Payment
    path('order',views.orderproduct,name='order'),
    path('order_history',views.order_history,name="order_history"),

]