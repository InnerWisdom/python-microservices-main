from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Prediction, User
from .producer import publish
from .serializers import PredictionSerializer
import random


class PredictionViewSet(viewsets.ViewSet):
    def list(self, request):
        predictions = Prediction.objects.all()
        serializer = PredictionSerializer(predictions, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PredictionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('prediction_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        prediction = Prediction.objects.get(id=pk)
        serializer = PredictionSerializer(prediction)
        return Response(serializer.data)

    def update(self, request, pk=None):
        prediction = Prediction.objects.get(id=pk)
        serializer = PredictionSerializer(instance=prediction, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('prediction_updated', serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        prediction = Prediction.objects.get(id=pk)
        prediction.delete()
        publish('prediction_deleted', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            'id': user.id
        })
