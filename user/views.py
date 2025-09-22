from django.shortcuts import render

from user import serializer as api_serializer
from user.models import User, Profile

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from notification.utils import create_notification


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = api_serializer.RegisterSerializer


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = api_serializer.UserSerializer(user)
        return Response(serializer.data)


class PublicProfileView(generics.RetrieveAPIView):
    queryset = Profile.objects.select_related('user')
    serializer_class = api_serializer.ProfileSerializer
    lookup_field = 'user_id'
    lookup_url_kwarg = 'id'

class MyProfileUpdateView(generics.UpdateAPIView):
    serializer_class = api_serializer.ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.users_profile


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        target_user = User.objects.filter(id=id).first()
        if not target_user or target_user == request.user:
            return Response({'message': 'Invalid operation, you cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.users_profile.following.add(target_user.users_profile)

        # Notify
        print("USER==>", target_user.users_profile)
        if request.user != target_user:
            verb = 'Followed by another user'
            create_notification(
                recipient=target_user,
                actor=request.user,
                verb=verb,
                target=target_user
            )
        return Response({
            'status': status.HTTP_200_OK,
            'message': f'Followed {target_user.username}',
            # 'data': serializer.data
        })

class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        target_user = User.objects.filter(id=id).first()
        if not target_user or target_user == request.user:
            return Response({'message': 'Invalid operation.'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.users_profile.following.remove(target_user.users_profile)

        # Notify
        print("USER==>", target_user.users_profile)
        if request.user != target_user:
            verb = 'Unfollowed by another user'
            create_notification(
                recipient=target_user,
                actor=request.user,
                verb=verb,
                target=target_user
            )
    
        return Response({
            'status': status.HTTP_200_OK,
            'message': f'Unfollowed {target_user.username}',
            # 'data': serializer.data
        })

class FollowersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        followers = request.user.users_profile.followers.all()
        serializer = api_serializer.ProfileSerializer(followers, many=True)
        return Response(serializer.data)

class FollowingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following = request.user.users_profile.following.all()
        serializer = api_serializer.ProfileSerializer(following, many=True)
        return Response(serializer.data)

