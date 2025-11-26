from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .utils import AIService

class PriceEstimationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        description = request.data.get("description", "")
        if not description:
            return Response({"error": "Description required"}, status=400)
            
        result = AIService.estimate_price(description)
        return Response(result)