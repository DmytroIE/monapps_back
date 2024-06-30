from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import post_save, post_delete
from common.constants import StatusTypes, CurrentStateTypes, StateStatusUse
from apps.nodes.models import Node

class Asset(models.Model):

    class Meta:
        db_table = "assets"

    name = models.CharField(max_length=200)

    # has_status = models.BooleanField() here we don't set it manually. If at least one children has a status propagated to its parent then the parent automatically has the status
    # has_current_state = models.BooleanField() the same as for the status (see above)
    status = models.IntegerField(default=None, choices=StatusTypes.choices, null=True, blank=True) # null=True because some apps can have no Status or Current state
    current_state = models.IntegerField(default=None, choices=CurrentStateTypes.choices, null=True, blank=True)
    prev_status = models.IntegerField(default=None, choices=StatusTypes.choices, null=True, blank=True)
    prev_current_state = models.IntegerField(default=None, choices=CurrentStateTypes.choices, null=True, blank=True)
    status_use = models.IntegerField(default=StateStatusUse.AS_IS, choices=StateStatusUse.choices)
    current_state_use = models.IntegerField(default=StateStatusUse.AS_IS, choices=StateStatusUse.choices)
    nodes = GenericRelation(Node, related_query_name='asset')
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Asset {self.name} id: {self.id}"
    
    def update_status_or_curr_state(self):
        node=self.nodes.filter(asset__pk=self.pk).first()
        if not node:
            return
        children_nodes = node.get_children()
        status_assumption = StatusTypes.UNDEFINED
        status_is_none_assumption = True
        current_state_assumption = CurrentStateTypes.UNDEFINED
        current_state_is_none_assumption = True
        for cn in children_nodes:
            obj = cn.content_object
            if obj.status and (obj.status_use != StateStatusUse.DONT_USE):
                status_is_none_assumption = False
                if obj.status > status_assumption:
                    if obj.status == StatusTypes.ERROR and obj.status_use == StateStatusUse.AS_WARNING:
                        status_assumption = StatusTypes.WARNING
                    else:
                        status_assumption = obj.status
            if obj.current_state and (obj.current_state_use != StateStatusUse.DONT_USE):
                current_state_is_none_assumption = False
                if obj.current_state > current_state_assumption:
                    if obj.current_state == CurrentStateTypes.ERROR and obj.current_state_use == StateStatusUse.AS_WARNING:
                        current_state_assumption = CurrentStateTypes.WARNING
                    else:
                        current_state_assumption = obj.current_state
        
        changed = False

        if status_is_none_assumption and self.status:
            changed = True
            self.status = None
        elif self.status != status_assumption:
            changed = True
            self.status = status_assumption

        if current_state_is_none_assumption and self.current_state:
            changed = True
            self.current_state = None
        elif self.current_state != current_state_assumption:
            changed = True
            self.current_state = current_state_assumption
        
        if changed:
            self.save()



def update_parent_from_asset(sender, instance, **kwargs):
    node=instance.nodes.filter(asset__pk=instance.pk).first()
    if node and not node.is_root():
        if (instance.status_use != StateStatusUse.DONT_USE and
            instance.prev_status != instance.status) \
            or \
           (instance.current_state_use != StateStatusUse.DONT_USE and 
            instance.prev_scurrent_state != instance.current_state):
            parent = node.get_parent()
            parent.content_object.update_status_or_curr_state()
            instance.prev_status = instance.status
            instance.prev_current_state = instance.current_state

post_save.connect(update_parent_from_asset, sender=Asset)
post_delete.connect(update_parent_from_asset, sender=Asset)