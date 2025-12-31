from django.db import models

class Comment(models.Model):
    comment_id = models.CharField(
        max_length=255, verbose_name='댓글 id'
    )
    video_id = models.CharField(max_length=255, verbose_name='동영상 id')
    authorDisplayName = models.CharField(max_length=100, verbose_name='작성자')
    authorChannelUrl = models.TextField(blank=True, verbose_name='작성자 채널 주소')
    textDisplay = models.TextField(blank=True, verbose_name='내용')
    textOriginal = models.TextField(blank=True, verbose_name='내용 원본')
    likeCount = models.IntegerField(verbose_name='좋아요 수')
    publishedAt = models.DateTimeField('작성일')
    updatedAt = models.DateTimeField('수정일')

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        db_table = 'comments'
        ordering = ['-likeCount']

    def __str__(self):
        return self.textOriginal