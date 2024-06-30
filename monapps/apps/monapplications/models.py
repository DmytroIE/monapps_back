from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django_celery_beat.models import PeriodicTask
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save, post_delete
from apps.nodes.models import Node
from common.constants import StatusTypes, CurrentStateTypes, StateStatusUse

class MonAppType(models.Model):
    class Meta:
        db_table = "monapptypes"

    name = models.CharField(max_length=200, blank = False, unique = True)
    description = models.CharField(max_length=1000, blank = True)
    path = models.CharField(max_length=200, blank = False, unique = True) # F.e. 'apps.monapplications.tasks.eval_trap_status_v1'
    input_ds_schema  = models.JSONField()
    # F.e. {"tempUpstream": {"verboseName":"Temperature upstream the heat exchanger", "type":"Temperature", "required": true}, "tankPressure": {...}}
    input_df_schema  = models.JSONField(blank=True)
    output_df_schema  = models.JSONField(blank=True)
    has_status = models.BooleanField()
    has_current_state = models.BooleanField()

    def __str__(self):
        return self.name


class MonApplication(models.Model):

    class Meta:
        db_table = "monapplications"

    UNDEFINED = 0
    STOPPED = 1
    CATCHING_UP = 2
    RUNNING = 3
    WARNING = 4
    ERROR = 5
    EXEC_STATE_CHOICES = {
        UNDEFINED: "Undefined",
        STOPPED: "Stopped",
        CATCHING_UP: "Catching up",
        RUNNING: "Running",
        WARNING: "Warning",
        ERROR: "Error",
    }

    type = models.ForeignKey(
        MonAppType,
        on_delete=models.PROTECT,
    )

    execution_state = models.IntegerField(
        choices=EXEC_STATE_CHOICES,
        default=STOPPED,
    )


    input_ds_schema = models.JSONField() # Should align with the values in self.type.input_ds_schema, f.e. {"tempUpstream": 125, ... where 125 is the id of a datastream
    input_df_schema = models.JSONField(blank=True) # Should align with the values in self.type.input_df_schema
    output_df_schema = models.JSONField(blank=True) # Should align with the values in self.type.output_df_schema
    status = models.IntegerField(default=StatusTypes.UNDEFINED, choices=StatusTypes.choices, null=True, blank=True) # null=True because some apps can have no Status or Current state
    current_state = models.IntegerField(default=CurrentStateTypes.UNDEFINED, choices=CurrentStateTypes.choices, null=True, blank=True)
    prev_status = models.IntegerField(default=StatusTypes.UNDEFINED, choices=StatusTypes.choices, null=True, blank=True)
    prev_current_state = models.IntegerField(default=CurrentStateTypes.UNDEFINED, choices=CurrentStateTypes.choices, null=True, blank=True)
    status_use = models.IntegerField(default=StateStatusUse.AS_IS, choices=StateStatusUse.choices)
    current_state_use = models.IntegerField(default=StateStatusUse.AS_IS, choices=StateStatusUse.choices)
    nodes = GenericRelation(Node, related_query_name='monapp')

    retain = models.JSONField(null=True, blank=True) # For retaining the state between calculations

    task = models.OneToOneField(PeriodicTask, 
                             on_delete = models.SET_NULL,
                             null = True,
                             blank = True,
                             default = None)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Mon app {self.name}"
    
    @property
    def name(self):
        return f"{self.type.name} id: {self.id}"


def update_parent_update_monapp(sender, instance, **kwargs):
    node=instance.nodes.filter(monapp__pk=instance.pk).first()
    if node and not node.is_root():
        if (instance.type.has_status and instance.status_use != StateStatusUse.DONT_USE and 
            instance.prev_status != instance.status) \
            or \
           (instance.type.has_current_state and instance.current_state_use != StateStatusUse.DONT_USE and \
            instance.prev_current_state != instance.current_state):
            parent = node.get_parent() # it always should be an asset
            parent.content_object.update_status_or_curr_state()
            instance.prev_status = instance.status
            instance.prev_current_state = instance.current_state

post_save.connect(update_parent_update_monapp, sender=MonApplication)
post_delete.connect(update_parent_update_monapp, sender=MonApplication)   