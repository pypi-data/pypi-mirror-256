DRF Flex Query
######

DRF Flex Query is an extension for [Django REST Framework](https://django-rest-framework.org/) which helps to speed up retrieving related objects of main query.

Using separate related objects query and python dicts instead of left joins in SQL and quering every related object using this package could speed up request with multiple related objects in several times.

Installation
============

You can install DRF Flex Query by:

.. code-block:: bash

    pip install drf-flex-query


Basic Usage
===========

Extend basic model
-------------

First of all you need to implement custom database manager by inherit from drf-flex-query manager:

.. code-block:: python

    from flex_query.models import Model

    class MyModel(Model):
        pass

    class MyQueringModel(Model):
        main_model = models.ForeignKey(MyModel, null=True)

    class MyRelatedModel(Model):
        main_model = models.ForeignKey(MyModel, null=True)


or you could add additional manager without changing relationship:

.. code-block:: python

    from django.db.models import Model

    from flex_query.manager import FlexQueryDBManager

    class MyModel(Model):
        flex_query_objects = FlexQueryDBManager()


Create serializer
=================

Define serializers for object and all relations:

.. code-block:: python

    from rest_framework.serializers import ModelSerializer

    from flex_query.serializers import FlexQueryBaseModelSerializer, RelatedAttrSerializerInfo

    class MainModelSerializer(ModelSerializer):

        class Meta:
            model = MyModel
            fields = "__all__"
    
    class MyRelatedModelSerializer(ModelSerializer):

        class Meta:
            model = MyRelatedModel
            fields = "__all__"

    class MySerializer(FlexQueryBaseModelSerializer):
        main_model = serializers.SerializerMethodField("get_main_model")
        related_models = serializers.SerializerMethodField("get_related_models")
    
        class Meta:
            model = MyQueringModel
            fields = ("id", "main_model", "related_models")
            custom_attrs = ("main_models", "related_models")
            related_attrs_mapping = {
                "get_main_model": RelatedAttrSerializerInfo(
                    dependency_name="main_models",
                    dep_field_map_name="main_model_id",
                    serializer_class=MainModelSerializer,
                    many=False,
                    forward_kwargs=(),
                ),
                "get_related_models": RelatedAttrSerializerInfo(
                    dependency_name="related_models",
                    dep_field_map_name="main_model_id",
                    serializer_class=MyRelatedModelSerializer,
                    many=True,
                    forward_kwargs=(),
                ),
            }


Define API View
===============

For setup APIView configuration you need to define list of related queries and rules for its quering

.. code-block:: python

    from flex_query.generics import FlexQueryRelationsGenericAPIView


    class MyAPIView(FlexQueryRelationsGenericAPIView):
        queryset = MyQueringModel.objects.all()
        serializer_class = MySerializer
        related_queries_data = [
            QueryFilterInfo(
                query_arg_name="main_models",
                attribute="main_model_id",
                query_model=MyModel,
                filter_field="pk",
                mapping_rules={1: KeyMapping(name="id", obj_type="object")},
            ),
            QueryFilterInfo(
                query_arg_name="related_models",
                attribute="id",
                query_model=MyRelatedModel,
                filter_field="pk",
                mapping_rules={1: KeyMapping(name="main_model_id", obj_type="list")},
                source_query="main_models",
            ),
        ]
