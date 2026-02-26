from django.db import models

class Story(models.Model):
    hn_id = models.IntegerField(unique=True, db_index=True)
    title = models.TextField(max_length=500)
    title_ko = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True)
    score = models.IntegerField(default=0)
    author = models.CharField(max_length=100)
    comment_count = models.IntegerField(default=0)
    fetched_at = models.DateTimeField(auto_now_add=True)
    hn_created_at = models.DateTimeField()

    class Meta:
        ordering = ['-score']

class HNComment(models.Model):
    hn_id = models.IntegerField(unique=True, db_index=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='comments')
    parent_id = models.IntegerField(null=True, blank=True)
    author = models.CharField(max_length=100)
    text = models.TextField()
    text_ko = models.TextField(blank=True)
    depth = models.IntegerField(default=0)
    hn_created_at = models.DateTimeField()

    class Meta:
        ordering = ['hn_created_at']