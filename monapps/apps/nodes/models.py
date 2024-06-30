from django.db import models
from treebeard.mp_tree import MP_Node
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Node(MP_Node):

    class Meta:
        db_table = "nodes"

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        if hasattr(self.content_object, 'name'):
            return f'{self.content_object.name} id: {self.content_object.id}'
        else:
            return 'Undefined'

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    