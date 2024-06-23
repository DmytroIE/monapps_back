from .constants import external_db_name

class ExternalDbRouter:
    """
    A router to control operations on the models 
    "device", "datastream", "reading"
    in the external database.
    """

    route_app_labels = {"devices", "datastreams", "readings"}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return external_db_name
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return external_db_name
        return None

    def allow_relation(self, obj1, obj2, **hints):
 
        if (
            obj1._meta.app_label in self.route_app_labels
            and obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            # return db == external_db_name
            return False
        # if db == external_db_name:
        #     return False

        return None