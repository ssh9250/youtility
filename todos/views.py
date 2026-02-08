from django.shortcuts import render
from rest_framework import viewsets

from todos.models import Todo
from todos.serializers import BaseTodoSerializer, TodoListSerializer, TodoCreateSerializer, TodoUpdateSerializer, \
    TodoDetailSerializer


# 비즈니스 로직 : basic crud, 완료/숨김 토글, 완료만/숨김만/모두 리스트로 보이기 처리
class TodoViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        include_hidden = self.request.query_params.get('hidden', 'false').lower() == 'true'
        base_queryset = Todo.objects.all()

        # todo: complete 토글 시 완료된 항목 보이기/숨기기 구현하기

        if include_hidden:
            return base_queryset
        else:
            return base_queryset.filter(hidden=False)

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

    # todo: 할일 뷰셋 작성 마저 진행
    # todo: include_hidden 토글 시 쿼리 어떻게 처리하는지 확인
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()