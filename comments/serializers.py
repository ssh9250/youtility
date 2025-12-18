from rest_framework import serializers
from .models import Comment


class BaseCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentCreateSerializer(BaseCommentSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        snippet = self.initial_data.get('snippet', {})

        for k in snippet:
            authorDisplayName = snippet.get('authorDisplayName')
            authorChannelUrl = snippet.get('authorChannelUrl')
            textDisplay = snippet.get('textDisplay')
            textOriginal = snippet.get('textOriginal')
            likeCount = snippet.get('likeCount')
            publishedAt = snippet.get('publishedAt')
            updatedAt = snippet.get('updatedAt')

