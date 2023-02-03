from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from .serializers import CollectionSerializer
from .models import Collection, Movies
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from helper.helper import add_request_counter
from django.core.signals import request_finished
# Create your views here.

class CollectionListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = CollectionSerializer(queryset, many=True)
        fav_genre = Movies.objects.filter(collection__user=request.user).order_by("-created")[:3].values_list(
            "genres", flat=True)
        request_finished.connect(add_request_counter)
        return Response({"is_success": True,
                        "data": {
                            "collections": serializer.data, 
                            "favourite_genres": list(fav_genre)
                            }
                        }
                        , status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.data
            movies_obj = validated_data.pop('movies')
            collection_obj = Collection.objects.create(**validated_data, user=self.request.user)
            print(collection_obj.uuid)
            for data in movies_obj:
                Movies.objects.create(
                    title=data["title"],
                    description=data["description"],
                    genres=data["genres"],
                    uuid=data["uuid"],
                    collection=collection_obj
                )
            request_finished.connect(add_request_counter)
            return Response({"uuid": collection_obj.uuid}, status=status.HTTP_200_OK)
        request_finished.connect(add_request_counter)
        return  Response(serializer.errors, status=status.HTTP_200_OK)
            
    

class CollectionUpdateView(UpdateAPIView, DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    
    def get_object(self, pk):
        try:
            collection = Collection.objects.get(uuid=pk)
            return collection
        except Collection.DoesNotExist:
            return None

    def put(self, request, pk):
        collection = self.get_object(pk)
        if not collection:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(collection, data=request.data)
        if serializer.is_valid():
            request_finished.connect(add_request_counter)
            return Response(serializer.data, status=status.HTTP_200_OK)
        request_finished.connect(add_request_counter)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        collection = self.get_object(pk)
        if not collection:
            request_finished.connect(add_request_counter)
            return Response(status=status.HTTP_404_NOT_FOUND)
        collection.delete()
        request_finished.connect(add_request_counter)
        return Response(
            {"message": f"collection with uuid {pk} deleted successfully"}, status=status.HTTP_200_OK)
    