from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Article, Comment
from .serializer import ArticleSerializer, ArticleDetailSerializer, CommentSerializer

from .permissions import IsCommentOwner

from notification.utils import create_notification 


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]  # Require login for modifying actions
        return [permissions.AllowAny()]
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Articles retrieved successfully',
            'data': serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        article = self.get_object()
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleCommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(article_id=self.kwargs['article_id'])

    def perform_create(self, serializer):
        article = Article.objects.get(pk=self.kwargs['article_id'])
        comment_author = self.request.user
        serializer.save(author=comment_author, article=article)

        # Notify article author if the commenter is not the author themselves
        if article.author != comment_author:
            verb="commented on your article"
            create_notification(
                recipient=article.author,
                actor=comment_author,
                verb=verb,
                target=article
            )

        return Response({
            'message': 'Comment added!!!',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class CommentUpdateDeleteAPIView(generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentOwner]
    http_method_names = ['patch', 'delete']

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
