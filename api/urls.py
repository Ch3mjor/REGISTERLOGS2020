from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import RequestLogViewSet, log_request

router = DefaultRouter()
router.register('logs', RequestLogViewSet)

app_name = 'api'
urlpatterns = [
    path('', log_request)
] + router.urls
