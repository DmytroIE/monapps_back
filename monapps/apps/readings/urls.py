from django.urls import path,register_converter
from .views import ReadingList, ReadingRetrieve
from .converters import DateTimeToUnixConverter

register_converter(DateTimeToUnixConverter, 'datetime')


urlpatterns = [
    path('', ReadingList.as_view()),
    path('<datetime:pk>/', ReadingRetrieve.as_view()),
]