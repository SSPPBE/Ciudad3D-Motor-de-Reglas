from django.forms import CharField
from rest_framework.serializers import Serializer, FileField

# Serializers define the API representation.
class SimulateByFileIn(Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']

class SimulateByDbIn(Serializer):
    block_name = CharField()
    class Meta:
        fields = ['block_name']        