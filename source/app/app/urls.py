from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from .views import UploadViewSet
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from adapter.core import MediaAPI

from adapter.geo.ProcessAPI import DownloadDwg, Health, Launch

router = routers.DefaultRouter()
urlpatterns = [
    path('', include(router.urls)),
    path('api/launch/', Launch.as_view()),
    path('api/download/', DownloadDwg.as_view()),
    path('health', Health.as_view()),
    # ,url(r'^download/(?P<path>.*)$', MediaAPI.download)
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)