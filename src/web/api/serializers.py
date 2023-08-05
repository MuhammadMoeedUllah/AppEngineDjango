from django.contrib.auth.models import User, Group
from web.ui.models import Scan, Dents
from rest_framework import serializers
from rest_framework.reverse import reverse

class DentsSerializer(serializers.ModelSerializer):
    #scan_id = serializers.PrimaryKeyRelatedField(queryset=Scan.objects.all(),many=False)

    class Meta:
        model = Dents
        fields = '__all__'

class ScanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Scan
        fields = '__all__'
