from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from django.db.models import QuerySet
from django.db.models.manager import Manager


@dataclass
class KeyMapping:
    name: str
    obj_type: Literal["list", "dict", "object"] = "list"
    only_attr: Optional[str] = None


class FlexQueryMaping(QuerySet):
    keys = {}

    def _list(self, item: Any, obj: list = [], **kwargs) -> list:
        res = set(obj)
        if kwargs.get("only_attr"):
            res.add(getattr(item, kwargs["only_attr"]))
        else:
            res.add(item)
        return list(res)

    @property
    def _list_default(self) -> list:
        return []

    def _object(self, item: Any, **kwargs) -> Any:
        return item

    @property
    def _object_default(self) -> None:
        return None

    def _dict(
        self,
        item: Any,
        iteration: int,
        obj: dict = {},
        **kwargs,
    ) -> dict:
        _, mapping = self._set_default(mapping=obj, item=item, iteration=iteration)
        return mapping

    @property
    def _dict_default(self) -> dict:
        return {}

    @staticmethod
    def _check_iterable(obj: Any) -> bool:
        if any(
            [
                isinstance(obj, list),
                isinstance(obj, tuple),
                isinstance(obj, set),
                isinstance(obj, QuerySet),
            ]
        ):
            return True
        return False

    def _get_attr(self, obj: Any, name: str) -> Any:
        if self._check_iterable(obj):
            return [self._typing_attr(getattr(o, name)) for o in obj]
        return self._typing_attr(getattr(obj, name))

    def _typing_attr(self, obj: Any) -> Any:
        if hasattr(obj, "all"):
            return obj.all()
        if callable(obj):
            return obj()
        return obj

    def _get_map_key(self, obj: Any, key: str) -> List[Union[int, str]]:
        for k in key.split("."):
            if not k:
                continue
            obj = self._get_attr(obj, k)
        return obj if self._check_iterable(obj) else [obj]

    def _set_default(self, mapping: dict, item: Any, iteration: int = 1) -> Tuple[bool, Any]:
        key = self.keys.get(iteration)
        if not key:
            return False, mapping
        key_val = self._get_map_key(item, key.name)
        for k in key_val:
            mapping[k] = getattr(self, f"_{key.obj_type}")(
                item=item,
                obj=mapping.get(k, getattr(self, f"_{key.obj_type}_default")),
                iteration=iteration + 1,
                only_attr=key.only_attr,
            )

        return True, mapping

    @property
    def mapping(self) -> dict:
        res_dict = dict()
        for item in self:
            _, res_dict = self._set_default(res_dict, item)

        return res_dict

    def get_mapping(self, keys: Dict[int, KeyMapping]) -> dict:
        self.keys = keys
        return self.mapping


FlexQueryDBManager = Manager.from_queryset(FlexQueryMaping)
