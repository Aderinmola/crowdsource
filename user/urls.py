from user import views as api_views
from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("login/", api_views.MyTokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("register/", api_views.RegisterView.as_view()),
    path("profile/", api_views.CurrentUserView.as_view()),

    path('<uuid:id>/', api_views.PublicProfileView.as_view(), name='public-profile'),
    path('me/', api_views.MyProfileUpdateView.as_view(), name='edit-profile'),
    path('<uuid:id>/follow/', api_views.FollowUserView.as_view(), name='follow-user'),
    path('<uuid:id>/unfollow/', api_views.UnfollowUserView.as_view(), name='unfollow-user'),
    path('me/followers/', api_views.FollowersListView.as_view(), name='followers-list'),
    path('me/following/', api_views.FollowingListView.as_view(), name='following-list'),

]
