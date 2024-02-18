import inspect
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional, Type, Union

from django.db.models import Model

from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.fields import Field, empty


@dataclass
class RelatedAttrSerializerInfo:
    dependency_name: str
    dep_field_map_name: str
    serializer_class: Serializer
    many: bool
    forward_kwargs: tuple


class FlexQueryBaseModelSerializer(ModelSerializer):
    _base_serializers_extra_kwargs = ("partial", "context", "many")

    class MockDependencySerializer:
        pass

    def __init__(self, instance=None, data=empty, **kwargs):
        self._dep_method_name: str = ""
        kwargs = self._set_addition_attrs(**kwargs)
        super().__init__(instance, data, **kwargs)

    def __getattr__(self, item: str) -> Any:
        if not re.match(r"get_[a-z]+", item):
            raise AttributeError("{} has not attribute {}".format(self.__class__.__name__, item))
        self._dep_method_name = item
        return self.get_custom_attr_value

    def _set_addition_attrs(self, **kwargs) -> dict:
        if hasattr(self.Meta, "custom_attrs"):
            for field in self.Meta.custom_attrs:
                if kwargs.get(field):
                    setattr(self, field, kwargs.pop(field))
        return self._remove_custom_attrs(**kwargs)

    def _remove_custom_attrs(self, **kwargs) -> dict:
        for k in kwargs.copy():
            if (
                k not in inspect.signature(Field.__init__).parameters.keys()
                and k not in self._base_serializers_extra_kwargs
            ):
                kwargs.pop(k)
        return kwargs

    def get_custom_attr_value(self, obj: Type[Model]) -> Optional[Union[dict, list]]:
        if not hasattr(self.Meta, "related_attrs_mapping"):
            return None
        field_info = self.Meta.related_attrs_mapping.get(self._dep_method_name)
        if not field_info:
            return None
        try:
            return self._get_relations_from_dep_info(obj, field_info)
        except AttributeError:
            return self._default_serialized_value(field_info.many)

    def _get_relations_from_dep_info(
        self, obj: Type[Model], field_info: RelatedAttrSerializerInfo
    ) -> Optional[Union[dict, list]]:
        dependency = getattr(self, field_info.dependency_name)
        dep_field_map_value = getattr(obj, field_info.dep_field_map_name)
        dep_objs = dependency.get(
            dep_field_map_value, self._default_serialized_value(field_info.many)
        )
        forward_kwargs = {
            kwarg: getattr(self, kwarg)
            for kwarg in field_info.forward_kwargs
            if getattr(self, kwarg, None)
        }
        return self._serialize_data(field_info, dep_objs, forward_kwargs)

    def _serialize_data(
        self,
        field_info: RelatedAttrSerializerInfo,
        dep_objs: Any,
        forward_kwargs: Dict[str, Any],
    ) -> Optional[Union[dict, list]]:
        if not dep_objs:
            return dep_objs
        if field_info.serializer_class == self.MockDependencySerializer:
            return dep_objs

        serializer = field_info.serializer_class(dep_objs, many=field_info.many, **forward_kwargs)
        return serializer.data

    def _default_serialized_value(self, many: bool) -> Optional[list]:
        if many:
            return []
        return None
