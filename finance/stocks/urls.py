from rest_framework.routers import DefaultRouter

from .views import HoldingViewSet

router = DefaultRouter()
# router.register(r"holdings", HoldingViewSet, basename="holding")

urlpatterns = router.urls
# config/urls.py에 추가:
#   path("api/stocks/", include("finance.stocks.urls")),
