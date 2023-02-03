from django.urls import path
from .views import MovieView

urlpatterns = [
    path('', MovieView.as_view()),
]

