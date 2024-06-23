from django.urls import path, include


urlpatterns = [
    path('devices/', include('apps.devices.urls')),
    path('datastreams/', include('apps.datastreams.urls')),
    path('readings/', include('apps.readings.urls')),
]