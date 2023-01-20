from http.client import HTTPResponse
import mimetypes
import os
import traceback
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.conf import settings
import urllib 

def download(request, path):
    filename = "./media/tmp/" + path
    print("media/tmp/" + path)
    response = None
    try:
        mime_type = mimetypes.guess_type(filename)
        a = os.path.exists(filename)
        fl = open(filename, 'r')
        response = HTTPResponse(fl)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
    except:
        traceback.print_exc()
    return response