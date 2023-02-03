from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView
from helper.helper import add_request_counter
from django.core.signals import request_finished

from .models import RequestCounter

# Create your views here.
class RequestCounterView(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        request = RequestCounter.objects.all().first()
        if request:
            request_finished.connect(add_request_counter)
            return Response({"requests": request.request_count}, status=status.HTTP_200_OK)
        else:
            request_finished.connect(add_request_counter)
            return Response({"requests": 0}, status=status.HTTP_200_OK)


class RequestCounterResetView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    def create(self, request):
        request = RequestCounter.objects.all().first()
        if request:
            request.request_count = 0
            request.save()
        request_finished.connect(add_request_counter)
        return Response({ "message": "request count reset successfully"}, status=status.HTTP_200_OK)