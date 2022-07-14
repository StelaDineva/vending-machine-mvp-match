from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'cost',
            'amount_available',
            'seller_id',
        ]


class OrderSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        fields = [
            'product',
            'amount',
        ]

    def validate(self, data: dict) -> dict:
        amount = data['product'].cost * data['amount']
        if self.context['request'].user.deposit < amount:
            raise serializers.ValidationError("User deposit is not sufficient")

        if data['product'].amount_available < amount:
            raise serializers.ValidationError("Product stock is not sufficient")

        return data
