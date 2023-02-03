from django.urls import path
from .views import CollectionListCreateView, CollectionUpdateView

urlpatterns = [
    path('', CollectionListCreateView.as_view()),
    path('<uuid:pk>', CollectionUpdateView.as_view()),
]