from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Article, Vote, Rating
from .serializers import VoteSerializer, RatingSerializer

from django.shortcuts import get_object_or_404


class ArticleVoteUpdateAPIView(generics.UpdateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']

    def get_object(self):
        # This prevents 404 by always returning a placeholder, since update_or_create is used
        return None

    def patch(self, request, *args, **kwargs):
        article_id = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vote_type = serializer.validated_data['vote_type']

        Vote.objects.update_or_create(
            user=request.user,
            article=article,
            defaults={'vote_type': vote_type}
        )
        return Response({'message': 'Vote registered'}, status=status.HTTP_200_OK)


class ArticleRatingUpdateAPIView(generics.UpdateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']

    def get_object(self):
        return None  # Not used directly

    def patch(self, request, *args, **kwargs):
        article_id = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        score = serializer.validated_data['score']

        Rating.objects.update_or_create(
            user=request.user,
            article=article,
            defaults={'score': score}
        )
        return Response({'message': 'Rating registered'}, status=status.HTTP_200_OK)



