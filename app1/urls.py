from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('booktable', views.booktable, name='booktable'),
            path('account' , views.account, name='account'),

    

    path('registration', views.registration, name='registration'),
       path('login', views.login, name='login'),
            path('logout', views.logout, name='logout'),
            path('cart', views.cart, name='cart'),
            path('addtoproduct', views.addtoproduct, name='addtoproduct'),

            path('addtocart/<int:id>', views.addtocart, name='addtocart'),
            path('checkout', views.checkout, name='checkout'),
            path('checkout', views.checkout, name='checkout'),
            path('confirmorder', views.confirmorder, name='confirmorder'),
            path('myorders' , views.myorders, name='myorders'),





            


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
