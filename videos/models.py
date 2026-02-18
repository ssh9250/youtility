from django.db import models


class Video(models.Model):
    video_id = models.CharField(max_length=255, verbose_name="동영상 id")
    title = models.CharField(max_length=255, verbose_name="동영상 제목")
    created_at = models.DateTimeField(auto_now_add=False)
    # ...

class Playlist(models.Model):
    playlist_id = models.CharField(max_length=255, verbose_name="재생목록 id")
    title = models.CharField(max_length=255, verbose_name="재생목록 제목")

class DownloadTask(models.Model):
    task_id = models.CharField(max_length=255)