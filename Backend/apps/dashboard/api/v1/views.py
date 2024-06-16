from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , permissions
from apps.dashboard.utils import get_device_datapoints_from_csv

class DashboardPieChartView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        datapoints = get_device_datapoints_from_csv('apps\scan\csv\IoTData.csv')
        return Response({"datapoints": datapoints}, status=status.HTTP_200_OK)
