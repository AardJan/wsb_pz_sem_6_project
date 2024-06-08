from django.urls import path
from .views import UserCreateView, CustomAuthToken, UserLogoutView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="user-register"),
    path("login/", CustomAuthToken.as_view(), name="user-login"),
    path("logout/", UserLogoutView.as_view(), name="user-logout"),
]
