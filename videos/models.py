from django.db import models


class Video(models.Model):
    # db_index = 인덱스 생성 후 이진탐색 -> 검색속도 향상
    video_id = models.CharField(max_length=255, unique=True, db_index=True, verbose_name="동영상 id")
    title = models.CharField(max_length=255, verbose_name="제목")
    duration = models.IntegerField(null=True, blank=True, verbose_name="길이(초)")
    thumbnail_url = models.URLField(blank=True, verbose_name="썸네일 URL")
    created_at = models.DateTimeField(auto_now_add=False)
    # ...
    class Meta:
        verbose_name = "비디오"
        verbose_name_plural = "비디오 목록"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class DownloadTask(models.Model):
    STATUS_CHOICES = [
        ('pending', '대기중'),
        ('processing', '처리중'),
        ('completed', '완료'),
        ('failed', '실패'),
    ]

    task_id = models.CharField(max_length=255, unique=True, verbose_name="작업 ID")
    playlist_url = models.URLField(verbose_name="재생목록 URL")
    playlist_title = models.CharField(max_length=255, blank=True, verbose_name="재생목록 제목")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="상태"
    )
    progress = models.IntegerField(default=0, verbose_name="진행률(%)")
    total_videos = models.IntegerField(default=0, verbose_name="전체 영상 수")
    completed_videos = models.IntegerField(default=0, verbose_name="완료된 영상 수")
    current_video_title = models.CharField(max_length=255, blank=True, verbose_name="현재 처리중인 영상")

    zip_file_path = models.CharField(max_length=500, blank=True, verbose_name="ZIP 파일 경로")
    error_message = models.TextField(blank=True, verbose_name="에러 메시지")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="완료일")

    class Meta:
        verbose_name = "다운로드 작업"
        verbose_name_plural = "다운로드 작업 목록"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.task_id} - {self.get_status_display()}"