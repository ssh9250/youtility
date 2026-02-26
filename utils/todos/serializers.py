from rest_framework import serializers
from .models import Todo


class BaseTodoSerializer(serializers.ModelSerializer):
    content = serializers.CharField(
        max_length=20,
    )

    class Meta:
        model = Todo
        fields = "__all__"


class TodoCreateSerializer(BaseTodoSerializer):
    pass

class TodoListSerializer(BaseTodoSerializer):
    pass

class TodoDetailSerializer(BaseTodoSerializer):
    pass

class TodoUpdateSerializer(BaseTodoSerializer):
    pass

class TodoDeleteSerializer(BaseTodoSerializer):
    pass
