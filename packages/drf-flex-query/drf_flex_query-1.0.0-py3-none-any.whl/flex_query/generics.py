import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

from django.db.models import Model, Q, QuerySet
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .manager import KeyMapping


@dataclass
class RelationModelMappingInfo:
    model: Model
    mapping_args: Dict[int, KeyMapping]
    filters: List[Q] = field(default_factory=list)
    select_related: List[str] = field(default_factory=list)
    prefetch_related: List[str] = field(default_factory=list)


@dataclass
class QueryFilterInfo:
    # Name of variable which will be defined as key in result dict
    # and pass to serializers
    query_arg_name: str
    attribute: str  # Name of field for collect filtering arr
    query_model: Model  # Model which will be source for queryset
    filter_field: str  # Name of filtering field
    mapping_rules: Dict[int, KeyMapping]
    # Define key of related objs map if this query related to non self.queryset object
    source_query: str = ""


class FlexQueryRelationsGenericAPIView(GenericAPIView):
    related_queries_data = list()
    response_obj = Response

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.res_queries: Dict[str, Dict[Union[str, int, uuid.UUID], Any]] = dict()
        self.res_queryset: Union[QuerySet, List[Model]] = list()

    def _get_relation_models_mapping(self, relation: RelationModelMappingInfo) -> dict:
        qs = relation.model.flex_query_objects.filter(*relation.filters)
        if relation.select_related:
            qs = qs.select_related(*relation.select_related)
        if relation.prefetch_related:
            qs = qs.prefetch_related(*relation.prefetch_related)
        return qs.get_mapping(relation.mapping_args)

    def _get_filter_arr(
        self, main_query: Union[List[Model], QuerySet], attr: str
    ) -> List[Union[str, int, uuid.UUID]]:
        return [getattr(rec, attr) for rec in main_query]

    def _split_related_queries_to_two_arrs(
        self,
    ) -> Tuple[List[QueryFilterInfo], List[QueryFilterInfo]]:
        """
        Split self.related_queries_data to 2 arrays:
        - 1st with ralations to self.queryset objects
        - 2nd with relations to related objects queries

        The main reason of this spliting that defining related_queries_data
        shouldn't be sensitive to order of relations info definition.
        So the solution is to split relations info to two arrs
        and iterate over main related query and then second loop over lost filters
        """
        list_1st = list()
        list_2nd = list()
        for query_info in self.related_queries_data:
            if query_info.source_query:
                list_2nd.append(query_info)
            else:
                list_1st.append(query_info)
        return list_1st, list_2nd

    def _set_query_from_related_query_map(self, query_info: QueryFilterInfo) -> List[Any]:
        source_info = [
            q for q in self.related_queries_data if q.query_arg_name == query_info.source_query
        ][0]
        if source_info.mapping_rules[1].obj_type != "list":
            return self.res_queries.get(query_info.source_query, {}).values()
        else:
            return [
                obj
                for arr in self.res_queries.get(query_info.source_query, {}).values()
                for obj in arr
            ]

    def _get_relation_model_from_query_info(
        self,
        query_info: QueryFilterInfo,
    ) -> Dict[Union[str, int, uuid.UUID], Any]:
        main_query = self.res_queryset
        if query_info.source_query:
            main_query = self._set_query_from_related_query_map(query_info)
        return self._get_relation_models_mapping(
            RelationModelMappingInfo(
                model=query_info.query_model,
                mapping_args=query_info.mapping_rules,
                filters=[
                    Q(
                        **{
                            f"{query_info.filter_field}__in": self._get_filter_arr(
                                main_query, query_info.attribute
                            )
                        }
                    )
                ],
            )
        )

    def _get_related_models_from_query_info_arr(
        self,
        related_query_info: List[QueryFilterInfo],
    ) -> None:
        for query_info in related_query_info:
            method = getattr(
                self,
                f"_get_{query_info.query_arg_name}",
                self._get_relation_model_from_query_info,
            )
            self.res_queries[query_info.query_arg_name] = method(query_info)

    def get_related_models(self) -> None:
        splited_queries_info = self._split_related_queries_to_two_arrs()
        for query in splited_queries_info:
            self._get_related_models_from_query_info_arr(query)

    def get_resulted_qs(self, pk: Optional[Union[str, int]]) -> Response:
        if not self.queryset.query.order_by:
            self.queryset = self.queryset.order_by("-created")
        if pk:
            self.queryset = self.queryset.filter(pk=pk)

        self.res_queryset = self.filter_queryset(self.get_queryset())

        if not pk:
            page = self.paginate_queryset(self.res_queryset)
            if page is not None:
                self.res_queryset = page
                self.response_obj = self.get_paginated_response

        self.get_related_models()
        if pk:
            self.res_queryset = self.queryset.first()
        serializer = self.get_serializer(
            self.res_queryset,
            many=not bool(pk),
            **self.res_queries,
        )
        return self.response_obj(serializer.data)

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.get_resulted_qs(kwargs.get("id"))
