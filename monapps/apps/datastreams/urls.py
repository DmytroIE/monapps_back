from django.urls import path
from .views import DatastreamList, DatastreamRetrieve

urlpatterns = [
    path('', DatastreamList.as_view()),
    path('<int:pk>/', DatastreamRetrieve.as_view()),
]