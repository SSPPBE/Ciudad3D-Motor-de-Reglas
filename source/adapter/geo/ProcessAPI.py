import os
import uuid
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.views import View

from adapter.geo.ProcessService import ProcessService
from adapter.geo.ProcessAPIMap import SimulateByFileIn
from adapter.core.DependencyService import dependencyService
import traceback
import json


# ViewSets define the view behavior.
class SimulateByFile(ViewSet):
    serializer_class = SimulateByFileIn

    def list(self, request):
        return Response("GET API")

    def post(self, request):
        response = {}
        try:
            data = request.FILES.get('file_uploaded')
            file_path = "tmp/" + str(uuid.uuid4()) + ".gpkg"
            path = default_storage.save(file_path, ContentFile(data.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            processService:ProcessService = dependencyService.get(ProcessService)
            result = processService.executeFromFile(tmp_file)
            response = JsonResponse(result)
        except:
            traceback.print_exc()

        return response

class Launch(View):

    def post(self, request):
        param = json.loads(request.body.decode("utf-8"))
        response = {}

        if ('apikey' not in request.headers or request.headers['apikey'] != os.getenv('API_KEY')):
            return HttpResponse('Not Authorized', status=403)

        try:
            processService:ProcessService = dependencyService.get(ProcessService)

            blocks = param['blocks'] if 'blocks' in param else []
            sections = param['sections'] if 'sections' in param else []
            full = param['full'] if 'full' in param else False
            output = "cd3" if 'export_cd3' in param else "basic"

            result = processService.execute(blocks, sections, full, output)
            response = JsonResponse(result, safe=False)
        except:
            traceback.print_exc()

        return response

class DownloadDwg(View):

    def post(self, request):
        param = json.loads(request.body.decode("utf-8"))
        response = {}

        if ('apikey' not in request.headers or request.headers['apikey'] != os.getenv('API_KEY')):
            return HttpResponse('Not Authorized', status=403)

        try:
            processService:ProcessService = dependencyService.get(ProcessService)

            blocks = [param['block']] if 'block' in param else []

            result = processService.execute(blocks, [], False, "dxf")
            response = JsonResponse(result, safe=False)
        except:
            traceback.print_exc()

        return response

class Health(View):

    def get(self, request):
        if request.body:
            return JsonResponse({"status": "Not found"}, status=404)

        return JsonResponse({"status": "available"}, status=200)
