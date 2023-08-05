# from django.contrib.auth.models import User, Group
from web.api.serializers import ScanSerializer, DentsSerializer
from web.ui.models import Scan, Dents
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class ScanPostView(APIView):

    def post(self, request, format=None):
        try:
            scanData = request.data['scan']
            dentData = request.data['dents']
        except Exception as e:
            return Response({"errors": "invalid data"})

        scan = ScanSerializer(data=scanData)

        if scan.is_valid():
            scan.save()
            dentData["scan_id"]=scan.data["id"]
            dents = DentsSerializer(data=dentData)
            #{"size_0_9": 4, "size_10_19": 21, "size_20_29": 34, "size_30_39": 87, "size_40_49": 23, "size_50_59": 42, "size_60_69": 18, "size_70_79": 1, "size_80_89": 3, "size_90_100": 0, "size_100_plus": 0}
            if dents.is_valid():
                dents.save()
                return Response(scan.data, status=status.HTTP_201_CREATED)
            return Response(dents.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(scan.errors, status=status.HTTP_400_BAD_REQUEST)

class ScanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows scan models to be viewed or edited.
    """
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer

class DentsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows dent models to be viewed or edited.
    """
    queryset = Dents.objects.all()
    serializer_class = DentsSerializer
