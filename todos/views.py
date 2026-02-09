from django.db.models import Count, Q
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from todos.models import Todo
from todos.serializers import BaseTodoSerializer, TodoListSerializer, TodoCreateSerializer, TodoUpdateSerializer, \
    TodoDetailSerializer


# 비즈니스 로직 : basic crud, 완료/숨김 토글, 완료만/숨김만/모두 리스트로 보이기 처리
class TodoViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        include_hidden = self.request.query_params.get('hidden', 'false').lower() == 'true'
        completed_param = self.request.query_params.get('completed')
        queryset = Todo.objects.all()

        if not include_hidden:
            queryset = queryset.filter(hidden=False)

        if completed_param is not None:
            is_completed = completed_param.lower() == 'true'
            queryset = queryset.filter(completed=is_completed)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return TodoListSerializer
        elif self.action == 'create':
            return TodoCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TodoUpdateSerializer
        elif self.action == 'retrieve':
            return TodoDetailSerializer
        return BaseTodoSerializer

    @action(detail=True, methods=['patch'], url_path='toggle')
    def toggle(self, request, pk=None):
        todo = self.get_object()
        todo.completed = not todo.completed
        todo.save()
        serializer = self.get_serializer(todo)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='hide')
    def hide(self, request, pk=None):
        todo = self.get_object()
        todo.hidden = not todo.hidden
        todo.save()
        serializer = self.get_serializer(todo)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        todos = self.get_queryset()

        stats = todos.aggregate(
            total_count=Count('id'),
            completed_count=Count('id', filter=Q(completed=True)),
            pending_count=Count('id', filter=Q(completed=False)),
        )

        return Response(stats)