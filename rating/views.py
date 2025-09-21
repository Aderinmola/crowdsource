from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Article, Vote, Rating
from .serializers import VoteSerializer, RatingSerializer

from django.shortcuts import get_object_or_404
from notification.utils import create_notification


class ArticleVoteUpdateAPIView(generics.UpdateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']

    def get_object(self):
        # This prevents 404 by always returning a placeholder, since update_or_create is used
        return None

    # def patch(self, request, *args, **kwargs):
    #     article_id = self.kwargs.get('pk')
    #     article = get_object_or_404(Article, pk=article_id)

    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     vote_type = serializer.validated_data['vote_type']

    #     Vote.objects.update_or_create(
    #         user=request.user,
    #         article=article,
    #         defaults={'vote_type': vote_type}
    #     )
    #     return Response({'message': 'Vote registered'}, status=status.HTTP_200_OK)
    

    def patch(self, request, *args, **kwargs):
        article_id = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vote_type = serializer.validated_data['vote_type']

        # Register or update the vote
        Vote.objects.update_or_create(
            user=request.user,
            article=article,
            defaults={'vote_type': vote_type}
        )
        print("USER===>", article.author)
        # Notify the article author
        if request.user != article.author:
            verb = 'upvoted your article' if vote_type == 'upvote' else 'downvoted your article'
            create_notification(
                recipient=article.author,
                actor=request.user,
                verb=verb,
                target=article
            )

        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Vote registered',
            'data': serializer.data
            })


class ArticleRatingUpdateAPIView(generics.UpdateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']

    def get_object(self):
        return None  # Not used directly

    def patch(self, request, *args, **kwargs):
        article_id = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_id)

        print("DEBUG — Article ID:", article.id)
        print("DEBUG — User ID:", request.user.id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        score = serializer.validated_data['score']

        Rating.objects.update_or_create(
            user=request.user,
            article=article,
            defaults={'score': score}
        )

        # Notify the article author
        if request.user != article.author:
            verb = 'rated your article'
            create_notification(
                recipient=article.author,
                actor=request.user,
                verb=verb,
                target=article
            )
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Rating registered',
            'data': serializer.data
            })
