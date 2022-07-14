import pytest
from django.contrib.auth.models import Group, Permission
from model_bakery import baker
from rest_framework.test import APIClient

from profiles.models import User


@pytest.fixture
def api_client():
    return APIClient


@pytest.fixture
def user_seller():
    group = Group.objects.create(name="seller")
    change_user_permissions = Permission.objects.filter(
        codename__in=["add_product", "change_product", "delete_product", "view_product"],
    )
    group.permissions.add(*change_user_permissions)
    return baker.make(User, is_active=True, groups=[group], deposit=0)


@pytest.fixture
def user_buyer():
    group = Group.objects.create(name="buyer")
    change_user_permissions = Permission.objects.filter(
        codename__in=["view_product", ],
    )
    group.permissions.add(*change_user_permissions)
    return baker.make(User, is_active=True, groups=[group], deposit=1000)
