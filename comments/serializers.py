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
