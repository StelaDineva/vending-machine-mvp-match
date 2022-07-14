from django.contrib.auth.models import AbstractUser
from django.db.models import IntegerField

from profiles.choices import DepositAllowedAmounts


class User(AbstractUser):
    deposit = IntegerField(default=0)

    def get_role(self):
        """
        Gets the user role.

        ToDo: Ensure only one role (Group) per user
        """
        return self.groups.first().name

    def split_by_coins(self) -> list:
        """
        Splits the user deposit amount by the most optimal coin configuration
        """
        change = []
        deposit = self.deposit
        for coin_value, _ in DepositAllowedAmounts.choices:
            count = deposit // coin_value
            for i in range(count):
                change.append(coin_value)
            deposit -= coin_value * count
        return change
