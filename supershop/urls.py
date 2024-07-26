"""
URL configuration for supershop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from mainapp import views as main
from mainapp import views as mainApp


#  for image uploding 
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',mainApp.homepage ,name="home"),
    path('about/',mainApp.aboutpage,name="about"),
    path('add-to-cart/',mainApp.addToCartPage,name="add-to-cart"),
    path('cart/',mainApp.cartpage,name="cart"),
    path('delete-cart/<str:id>/',mainApp.deleteCart,name="delete-cart"),
    path('update-cart/<str:id>/<str:op>/',mainApp.updateCartpage,name="update-cart"),
    path('checkout/',mainApp.checkoutpage,name="checkout"),
    path('re-payment/<int:id>/',mainApp.rePaymentpage,name="rePayment"),
    path('payment-success/<int:id>/<str:rppid>/<str:rpoid>/<str:rpsid>/',mainApp.paymentSuccesspage,name="payment-success"),
    path('confirmation/',mainApp.confirmationpage,name="confirmation"),
    path('contact/',mainApp.contactpage,name="contact"),
    path('login/',mainApp.loginpage,name="login"),
    path('logout/',mainApp.logoutpage,name="logout"),
    path('signup/',mainApp.signuppage,name="signup"),
    path('shop/<str:mc>/<str:sc>/<str:br>/',mainApp.shoppage,name="shop"),
    path('singleproduct/<int:id>/',mainApp.singleproductpage,name="singleproduct"),
    path('profile/',mainApp.profilepage,name="profile"),
    path('updateprofilez/',mainApp.updateprofilepage,name="update-profile"),
    path('add-to-wishlist/<int:id>/',mainApp.addToWishlistpage,name="addToWishlistpage"),
    path("delete-wishlist/<int:id>/",mainApp.deletewishlistpage),
    path("newslatter/subscribe/",mainApp.newslatteSubscribePage, name="newslatter-subscribe"),
    path('search/',mainApp.searchPage,name="search"),

    path('forget_password_1/',mainApp.forgetPassword1Page,name="forget_password_1"),
    path('forget_password_2/',mainApp.forgetPassword2Page,name="forget_password_2"),
    path('forget_password_3/',mainApp.forgetPassword3Page,name="forget_password_3"),



    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



