from django.contrib.auth.models import Group
from rest_framework import serializers


class RoleField(serializers.StringRelatedField):
    def to_internal_value(self, value: str) -> Group:
        try:
            return Group.objects.get(name=value)
        except (Group.DoesNotExist, Group.MultipleObjectsReturned):
            raise serializers.ValidationError(f"Sector with name: {value} not found")
