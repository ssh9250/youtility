from django.urls import path, include
from rest_framework import routers

from .views import VideoViewSet, DownloadTaskViewSet

router = routers.DefaultRouter()
router.register("", VideoViewSet, basename="video")
router.register("downloads", DownloadTaskViewSet, basename="download-task")

urlpatterns = [
    path("", include(router.urls)),
]