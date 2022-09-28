from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/home/')),
    path('login/', views.user_login),
    path('login/submit', views.submit_login),
    path('logout/', views.user_logout),
    path('home/', views.home),
]