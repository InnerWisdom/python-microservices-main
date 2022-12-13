from django.test import TestCase
from .models import Prediction
from .serializers import PredictionSerializer


class PredictTestCase(TestCase):
    def listTest(self):
        predictions = Prediction.objects.all()
        serializer = PredictionSerializer(predictions, many=True)
        self.assertEqual(serializer)

    def createTest(self, request):
        serializer = PredictionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.assertEqual(serializer)

    def retrieveTest(self, pk=None):
        prediction = Prediction.objects.get(id=pk)
        serializer = PredictionSerializer(prediction)
        self.assertEqual(serializer)

    def updateTest(self, request, pk=None):
        prediction = Prediction.objects.get(id=pk)
        serializer = PredictionSerializer(instance=prediction, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.assertEqual(serializer)

    def destroyTest(self, pk=None):
        prediction = Prediction.objects.get(id=pk)
        prediction.delete()
        self.assertEqual(prediction)
