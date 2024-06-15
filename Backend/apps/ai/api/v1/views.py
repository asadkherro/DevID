from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from apps.ai.utils import predict_device_category , get_sample_inputs

class PredictDeviceCategoryView(APIView):
    permission_classes = [AllowAny]

    def post(self , request):
        input_dict = get_sample_inputs()
        response = []
        for key , value in input_dict.items():
            data = value
            print(len(value))
            while len(data) < 297:
                data.append(0)
            prediction_output = predict_device_category(data)
            response.append(
                {
                    "expected_output" : key,
                    "predicted_output" : prediction_output
                }
            )
        return Response(response , status=status.HTTP_200_OK)