from django.core.exceptions import ValidationError


def validate_cost(value: int) -> None:
    """
    Validates that the Model field is divisible by 5
    """
    if value % 5 != 0:
        raise ValidationError(
            '%(value)s should be in multiples of 5',
            params={'value': value},
        )
