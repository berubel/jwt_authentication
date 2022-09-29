from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/home/')),
    path('login/', views.user_login),
    path('login/submit', views.submit_login),
    path('logout/', views.user_logout),
    path('home/', views.home),
    path('jwt_login/', views.jwt_user_login),
    path('jwt_user/', views.jwt_user_view),
    path('jwt_logout/', views.jwt_user_logout),
]