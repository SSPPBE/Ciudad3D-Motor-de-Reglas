from django.http.response import HttpResponse, JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import UploadSerializer
from wsgiref.util import FileWrapper
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

import uuid
import os
import sys
import inspect
import mimetypes

#currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#parentdir = os.path.dirname(currentdir)
#parentdir = os.path.dirname(parentdir)
#sys.path.insert(0, parentdir) 

from adapter.geo.ProcessService import ProcessService

# ViewSets define the view behavior.
class UploadViewSet(ViewSet):
    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def post(self, request):
        data = request.FILES.get('file_uploaded')
        file_path = "tmp/" + str(uuid.uuid4()) + ".gpkg"
        output_name = str(uuid.uuid4()) + ".gpkg"
        output_path = "media/tmp/" + output_name
        path = default_storage.save(file_path, ContentFile(data.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        process = ProcessImpl()
        process.execute(tmp_file, output_path)
        response = JsonResponse({"url":"/download/" + output_name})
        return response
