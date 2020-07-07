
from rest_framework.serializers import ModelSerializer

from api.models import Computer


class ComputerModelSerializer(ModelSerializer):

    class Meta:
        model = Computer
        fields = ('name',"price","brand")