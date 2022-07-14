from django.db import models

from products.validators import validate_cost


class Product(models.Model):
    name = models.CharField(max_length=1000, unique=True, help_text="Item full name")
    cost = models.PositiveIntegerField(validators=[validate_cost], help_text="Cost per product in cents")
    amount_available = models.PositiveIntegerField(default=0, help_text="Amount of items (default:0)")
    seller_id = models.CharField(max_length=100, help_text="Seller identifier")
