from django.db import models

# https://stackoverflow.com/questions/1117564/set-django-integerfield-by-choices-name
class StatusTypes(models.IntegerChoices):
    UNDEFINED = 0, 'Undefined'
    OK = 1, 'OK'
    WARNING = 2, 'Warning'
    ERROR = 3, 'Error'


class CurrentStateTypes(models.IntegerChoices):
    UNDEFINED = 0, 'Undefined'
    OK = 1, 'OK'
    WARNING = 2, 'Warning'
    ERROR = 3, 'Error'

class StateStatusUse(models.IntegerChoices):
    DONT_USE = 0, "Don't use at all"
    AS_WARNING = 1, 'All as warning'
    AS_IS = 2, 'As is'
