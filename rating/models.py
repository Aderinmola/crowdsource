from django.db import models
# from django.contrib.auth import get_user_model
from user.models import User
from article.models import Article
import uuid

# User = get_user_model()

class Vote(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    UPVOTE = 'upvote'
    DOWNVOTE = 'downvote'

    VOTE_CHOICES = [
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.CharField(max_length=20, choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'article')  # One vote per user per article


class Rating(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    SCORE_CHOICES = [(i, str(i)) for i in range(1, 6)]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        to_field='id',  # Make it explicit
        db_column='user_id'
        )
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE,
        to_field='id',  # Make it explicit
        db_column='article_id',
        related_name='ratings'
        )
    score = models.IntegerField(choices=SCORE_CHOICES)

    class Meta:
        unique_together = ('user', 'article')  # Ensure one rating per user per article
