from django.urls import path
from .views import RequestCounterView,RequestCounterResetView

urlpatterns = [
    path('', RequestCounterView.as_view()),
    path('reset/', RequestCounterResetView.as_view()),
]
