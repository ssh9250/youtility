from django.db import models


class Comment(models.Model):
    comment_id = models.CharField(max_length=255, verbose_name="댓글 id")
    video_id = models.CharField(max_length=255, verbose_name="동영상 id")
    author_display_name = models.CharField(max_length=100, verbose_name="작성자")
    author_channel_url = models.TextField(blank=True, verbose_name="작성자 채널 주소")
    text_display = models.TextField(blank=True, verbose_name="내용")
    text_original = models.TextField(blank=True, verbose_name="내용 원본")
    like_count = models.IntegerField(verbose_name="좋아요 수")
    published_at = models.DateTimeField("작성일")
    updated_at = models.DateTimeField("수정일")

    class Meta:
        verbose_name = "댓글"
        verbose_name_plural = "댓글 목록"
        db_table = "comments"
        ordering = ["-like_count"]

    def __str__(self):
        return self.text_original
