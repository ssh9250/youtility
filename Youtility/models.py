from django.db import models


class Video(models.Model):
    video_id = models.CharField(max_length=255, verbose_name="동영상 id")
    # ...

class Playlist(models.Model):
    playlist_id = models.CharField(max_length=255, verbose_name="재생목록 id")