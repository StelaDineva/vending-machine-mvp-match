from django.db import IntegrityError, transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.permissions import BuyerPermission, SellerPermission
from api.serializers.products import ProductSerializer, OrderSerializer
from products.models import Product


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD endpoint for Product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, SellerPermission]

    def get_permissions(self):
        if self.action in ["buy"]:
            return [IsAuthenticated(), BuyerPermission()]

        if self.action in ["list", None]:
            return [IsAuthenticated(), ]

        return super().get_permissions()

    @action(methods=['post'], detail=False)
    def buy(self, request: Request) -> Response:
        """
        Users with a “buyer” role can buy a product.
        (shouldn't be able to buy multiple different products at the same time) with the money they’ve deposited.

        Returns the total they’ve spent, the product they’ve purchased and their change if there’s any
         (in an array of 5, 10, 20, 50 and 100 cent coins)
        """
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        product = serializer.validated_data['product']
        purchased_amount = serializer.validated_data['amount']
        try:
            with transaction.atomic():
                products_cost = product.cost * purchased_amount
                request.user.deposit = request.user.deposit - products_cost
                request.user.save()
                product.amount_available = product.amount_available - purchased_amount
                product.save()
        except IntegrityError:
            return Response({"deposit": "Deposit is not sufficient"}, status=400)

        return Response({
            'change': request.user.split_by_coins(),
            'amount_spent': products_cost,
            "product": f"{purchased_amount} x {product.name}"
        })
