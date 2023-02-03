"""oneFin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# http://localhost:8000/register/ -- Post -- done
# http://localhost:8000/movies/ -- get -- done
# http://localhost:8000/collection/ -- get  -- done
# http://localhost:8000/collection/ -- post -- done
# http://localhost:8000/collection/<collection_uuid>/ -- put -- Done
# http://localhost:8000/collection/<collection_uuid>/ -- Delete -- Done
# http://localhost:8000/request-count/ -- get
# http://localhost:8000/request-count/reset/ -- post

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('registerApp.urls')),
    path('movies/', include('movieApp.urls')),
    path('collection/', include('collectionApp.urls')),
    path('request-count/', include('requestCountApp.urls')),
    
]