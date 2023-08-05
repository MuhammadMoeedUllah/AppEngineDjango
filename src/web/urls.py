from django.urls import include, path
from rest_framework import routers
from web.api import views

urlpatterns = [
    path('api/', include('web.api.urls')),
    path('app/', include('web.ui.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
