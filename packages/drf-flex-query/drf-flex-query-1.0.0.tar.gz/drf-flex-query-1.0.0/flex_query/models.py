from django.db.models import Model as DjangoModel

from .manager import FlexQueryDBManager


class Model(DjangoModel):
    objects = FlexQueryDBManager()
    flex_query_objects = objects
