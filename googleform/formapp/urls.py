
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('register/',views.register , name='register'),
    path('signin/',views.signin, name='signin'),
    path('home/',views.home , name='home'),
    path('signout/',views.signout , name='signout'),
    path('activation/<uidb64>/<token>', views.activation , name='activation'),
]
