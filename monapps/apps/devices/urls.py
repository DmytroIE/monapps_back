from django.urls import path
from .views import DeviceList, DeviceRetrieve

urlpatterns = [
    path('', DeviceList.as_view()),
    path('<int:pk>/', DeviceRetrieve.as_view()),
]