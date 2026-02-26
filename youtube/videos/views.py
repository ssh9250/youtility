import uuid

from rest_framework import viewsets

from youtube.videos.models import Video, DownloadTask
from youtube.videos.serializers import VideoSerializer, DownloadTaskSerializer, DownloadTaskCreateSerializer, \
    DownloadTaskStatusSerializer


# Create your views here.
class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'video_id'

class DownloadTaskViewSet(viewsets.ModelViewSet):
    queryset = DownloadTask.objects.all()
    serializer_class = DownloadTaskSerializer
    lookup_field = 'task_id'

    def get_serializer(self):
        if self.action == 'create':
            return DownloadTaskCreateSerializer
        elif self.action == 'status':
            return DownloadTaskStatusSerializer

        return DownloadTaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        playlist_url = serializer.validate_data['playlist_url']

        task_id = str(uuid.uuid4())

        task = DownloadTask.objects.create(
            task_id = task_id,
            playlist_url = playlist_url,
            status = 'pending',
        )