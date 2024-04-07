from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , permissions
from .utils import get_device_datapoints_from_csv  # Import your function

class DashboardPieChartView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        datapoints = get_device_datapoints_from_csv('scan\csv\IoTData.csv')
        return Response({"datapoints": datapoints}, status=status.HTTP_200_OK)
