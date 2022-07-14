from django.contrib.auth.models import Group
from django.db import models
from rest_framework import serializers

from api.fields import RoleField
from profiles.choices import DepositAllowedAmounts
from profiles.models import User


class ProfileSerializer(serializers.ModelSerializer):
    class ProfileRoles(models.TextChoices):
        SELLER = 'seller'
        BUYER = 'buyer'

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
    )
    password_repeat = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
    )
    role = RoleField(many=True, source="groups", default=Group.objects.filter(name=ProfileRoles.BUYER.value))

    deposit = serializers.CharField(
        read_only=True,
        help_text='Deposit Amount',
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password_repeat',
            'role',
            'deposit'
        ]

    def validate(self, data: dict) -> dict:
        password_repeat = data.pop('password_repeat')
        password = data['password']
        if password != password_repeat:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data: dict) -> dict:
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user


class DepositSerializer(serializers.Serializer):
    amount = serializers.ChoiceField(choices=DepositAllowedAmounts.choices)
