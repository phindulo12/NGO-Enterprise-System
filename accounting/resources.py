from import_export import resources
from .models import data


class DataResource(resources.ModelResource):
    class meta:
        model = data