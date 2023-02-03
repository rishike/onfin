from requestCountApp.models import RequestCounter
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from rest_framework.throttling import UserRateThrottle
import base64
from rest_framework.permissions import IsAuthenticated
from helper.helper import add_request_counter, retry
from django.core.signals import request_finished
from django.conf import settings
# Create your views here.

FETCH_API = settings.FETCH_API
USERNAME = settings.USERNAME
PASSWORD = settings.PASSWORD
PATH = "/movies/"

class MovieView(APIView):
    # throttle_classes = [UserRateThrottle]
    permission_classes = (IsAuthenticated,)
    
    @retry(times=3, exceptions=(ValueError, TypeError, Exception))
    def get(self, request, format=None):
        CURRENT_URL = request.get_host() + PATH
        edata = USERNAME+":"+PASSWORD
        edata=base64.b64encode(edata.encode())
        params = self.request.query_params.get('page')
        payload={}
        headers = {
            'Authorization': 'Basic '+edata.decode()
            }
        qp = "?page="+params if params is not None else "" 
        movies_data = requests.request("GET", FETCH_API+qp, headers=headers, data=payload)
        movies_data =  movies_data.json()
        if movies_data.get('is_success') == False:
            return Response(movies_data, status=200)

        results = movies_data['results']
        count = movies_data['count']
        next = movies_data['next'].replace(FETCH_API, CURRENT_URL) if movies_data.get('next') else None
        previous = movies_data['previous'].replace(FETCH_API, CURRENT_URL) if movies_data.get('previous') else None
        request_finished.connect(add_request_counter)
        return Response({'count': count,
                         'next': next,
                         'previous': previous,
                         'results': results}
        , status=200)