from django.db import models
# from django.contrib.auth import get_user_model
from user.models import User
from article.models import Article


# User = get_user_model()

class Vote(models.Model):
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
    SCORE_CHOICES = [(i, str(i)) for i in range(1, 6)]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(choices=SCORE_CHOICES)

    class Meta:
        unique_together = ('user', 'article')  # Ensure one rating per user per article

