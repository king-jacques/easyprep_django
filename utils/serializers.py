from rest_framework import serializers
from django.db.models import Model
from django.db.models.query import QuerySet
from django.db import models
import uuid
from django.core.exceptions import ValidationError
class FlexibleSerializer(serializers.ModelSerializer):
    """
    Serializer class for flexible field definitions, allowing
    dynamically adding/removing of fields without needing to make
    a new serializer.
    """
    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(FlexibleSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    def apply_and_save(self, instance, data):
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.save()

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(FlexibleSerializer, self).get_field_names(declared_fields, info)
        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class GenericSerializer:
    ''' 
        Generic serializer that serializes any queryset or instance
        PARAMS
        * stringify: return string values for fields like UUID, boolean
        * many_to_many: include fields with have many to many relations
        * concat_many_to_many: return many to many fields as comma separated values of respective pks
    
    
    '''
    def __init__(self, data, fields=None, exclude=None, stringify=False, many_to_many=False, concat_many_to_many=True):
        self.queryset = data
        many = isinstance(data, QuerySet)
        self.many = many
        self.model = data.model if many else data._meta.model
        self.fields = fields or []
        self.exclude = exclude or []
        self.stringify = stringify
        self.many_to_many = many_to_many
        self.concat_many_to_many = concat_many_to_many


    @staticmethod
    def model_serializer(model_class, fields=None, exclude=None, stringify=False, many_to_many=False, concat_many_to_many=False):
        chosen_fields = fields or '__all__'
        excluded_fields = exclude or []

        many_to_many_fields = [field.name for field in model_class._meta.get_fields() if isinstance(field, models.ManyToManyField)]

        if not many_to_many:
            excluded_fields = excluded_fields + many_to_many_fields #excluded_fields += many_to_many_fields was mutating the original list            

        class ModelSerializer(serializers.ModelSerializer):

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                if many_to_many and concat_many_to_many:
                    for field_name in many_to_many_fields:
                        self.fields[field_name] = serializers.SerializerMethodField()
                        setattr(self, f'get_{field_name}', self.create_getter(field_name))

            def create_getter(self, field_name):
                def getter(instance):
                    many_to_many_values = getattr(instance, field_name).values_list('guid', flat=True)
                    return [str(value) for value in many_to_many_values]
                return getter

            def create(self, validated_data):
                model = self.Meta.model
                if isinstance(validated_data, list):
                    return model.objects.bulk_create([model(**item) for item in validated_data])
                return super().create(validated_data)
            
            def validate_guid(self, value):
                errors = []
                if not self.is_valid_uuid(value):
                    errors.append("The GUID is not a valid UUID format.")
                
                if self.Meta.model.objects.filter(guid=value).exists():
                    errors.append(f"{self.Meta.model.__name__} with this guid already exists.")
                
                if errors:
                    raise serializers.ValidationError({'guid': errors})
                return value or uuid.uuid4()

            def is_valid_uuid(self, value):
                """Check if the provided value is a valid UUID."""
                try:
                    uuid.UUID(str(value))
                    return True
                except ValueError:
                    return False
                
            def to_internal_value(self, data):
                if isinstance(data, list):
                    validated_data = []
                    for i, item in enumerate(data):
                        if not isinstance(item, dict):
                            raise serializers.ValidationError("Each item in the list must be a dictionary.")

                        item_data = super().to_internal_value(item)
                        guid = item.get('guid')
                        if guid:
                            item_data['guid'] = self.validate_guid(guid)

                        validated_data.append(item_data)
                    return validated_data
                else:
                    validated_data = super().to_internal_value(data)
                    guid = data.get('guid')
                    if guid:
                        validated_data['guid'] = self.validate_guid(guid)
                    return validated_data
                    
            def to_representation(self, instance):
                representation = super().to_representation(instance)
                if stringify:
                    representation = {field: str(value) if isinstance(value, uuid.UUID) else value for field, value in representation.items()}
                return representation

            class Meta:
                model = model_class
                if excluded_fields:
                    exclude = excluded_fields
                else:
                    fields = chosen_fields
        return ModelSerializer
    
    @property
    def serializer_class(self):
        serializer_class = self.model_serializer(self.model, self.fields, self.exclude, self.stringify, self.many_to_many, self.concat_many_to_many)
        return serializer_class
    
    @property
    def serializer(self):
        serializer_class = self.serializer_class
        serializer = serializer_class(self.queryset, many=True) if self.many else serializer_class(self.queryset)
        return serializer
    
    @property
    def data(self):
        return self.serializer.data
    