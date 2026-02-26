from django.db import models

class Todo(models.Model):
    content = models.CharField(max_length=20, null=False, blank=False, verbose_name="할일", default="내용을 입력하세요.")
    description = models.TextField(verbose_name='상세 설명')
    completed = models.BooleanField(default=False, verbose_name='완료 여부')
    hidden = models.BooleanField(default=False, verbose_name='숨김 여부')
    created = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    updated = models.DateTimeField(auto_now=True, verbose_name= "수정일")

    class Meta:
        verbose_name = "할 일"
        verbose_name_plural = "할 일 목록"
        ordering = ["-created"]

    def __str__(self):
        return self.content