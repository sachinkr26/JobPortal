from rest_framework.serializers import ModelSerializer
from testapp.models import hydjobs, punejobs, blorejobs, chennaijobs


class HydJobsSerializer(ModelSerializer):
    class Meta:
        model = hydjobs
        fields = '__all__'


class PuneJobsSerializer(ModelSerializer):
    class Meta:
        model = punejobs
        fields = '__all__'


class BloreJobsSerializer(ModelSerializer):
    class Meta:
        model = blorejobs
        fields = '__all__'


class ChennaiJobsSerializer(ModelSerializer):
    class Meta:
        model = chennaijobs
        fields = '__all__'
