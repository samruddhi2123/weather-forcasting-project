from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('weather/', views.weather_view, name="weather"),
    path('login/', auth_views.LoginView.as_view(template_name='weather_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
]
