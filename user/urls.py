from user import views as api_views
from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("login/", api_views.MyTokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("register/", api_views.RegisterView.as_view()),
    path("profile/", api_views.CurrentUserView.as_view()),
]