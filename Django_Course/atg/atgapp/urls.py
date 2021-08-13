from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='Home'),
    path("signin",views.signin,name="signin"),
    path("signup",views.signup,name="signup"),
    path("signout",views.signout,name="signout"),
    path("activate/<uidb64>/<token>",views.activate,name="activate"),
]