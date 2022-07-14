from django.db.models import IntegerChoices


class DepositAllowedAmounts(IntegerChoices):
    HUNDRED = 100
    FIFTY = 50
    TWENTY = 20
    TEN = 10
    FIVE = 5
