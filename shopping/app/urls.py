from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart,name="show_cart"),
    path('pluscart/',views.plus_cart,name="plus_cart"),
    path('minuscart/', views.minus_cart, name="minus_cart"),
    path('removecart/', views.remove_cart, name="remove_cart"),

    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='payment_done'),



    ##login and registor and reset and change

    path('changepassword/',views.changepass,name='changepassword'),

    path('changepassworddone/',views.changepas_done,name='changepassworddone'),
    path('registration/',views.customerregistration,name='customerregistration'),
    path('success/',views.success,name='success'),
    path('token/',views.token_send,name='token'),
    # path('error/',views.error,name='error'),
    path('account-verify/<slug:auth_token>',views.verify,name='verify'),
    path('accounts/login/',views.Login, name='login'),
    path('logout/',views.signout, name='logout'),


] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
