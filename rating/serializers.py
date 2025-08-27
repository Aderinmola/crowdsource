from rest_framework import serializers
from .models import Vote, Rating

class VoteSerializer(serializers.ModelSerializer):
    vote_type = serializers.ChoiceField(choices=[('upvote', 'Upvote'), ('downvote', 'Downvote')])

    class Meta:
        model = Vote
        fields = ['vote_type']

class RatingSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Rating
        fields = ['score']
