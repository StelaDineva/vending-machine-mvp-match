import json

import pytest
from model_bakery import baker

from products.models import Product

pytestmark = pytest.mark.django_db


class TestProductBuyEndpoint:
    endpoint = '/api/products/buy/'

    def test_buy_unauthenticated(self, api_client):
        product = baker.make(Product)
        data = {
            "product": product.id,
            "amount": 1
        }

        response = api_client().post(self.endpoint, data=data)

        assert response.status_code == 401

    def test_buy_seller(self, api_client, user_seller):
        product = baker.make(Product, cost=10)
        data = {
            "product": product.id,
            "amount": 1
        }

        client = api_client()
        user_seller.deposit = 10
        user_seller.save()
        client.force_authenticate(user=user_seller)
        response = client.post(self.endpoint, data=data)
        assert response.status_code == 403

    def test_buy_buyer_insufficient_deposit(self, api_client, user_buyer):
        product = baker.make(Product, cost=10, amount_available=10)
        data = {
            "product": product.id,
            "amount": 1
        }

        client = api_client()
        user_buyer.deposit = 8
        client.force_authenticate(user=user_buyer)
        response = client.post(self.endpoint, data=data)
        assert response.status_code == 400

    def test_buy_buyer_exact_deposit(self, api_client, user_buyer):
        product = baker.make(Product, cost=10, amount_available=10)
        data = {
            "product": product.id,
            "amount": 1
        }

        client = api_client()
        user_buyer.deposit = 10
        user_buyer.save()
        client.force_authenticate(user=user_buyer)
        response = client.post(self.endpoint, data=data)
        assert response.status_code == 200
        assert json.loads(response.content)['change'] == []

    def test_buy_buyer_more_deposit(self, api_client, user_buyer):
        product = baker.make(Product, cost=10, amount_available=10)
        data = {
            "product": product.id,
            "amount": 1
        }

        client = api_client()
        user_buyer.deposit = 195
        user_buyer.save()
        client.force_authenticate(user=user_buyer)
        response = client.post(self.endpoint, data=data)
        assert response.status_code == 200
        assert json.loads(response.content)['change'] == [100, 50, 20, 10, 5]

    def test_buy_buyer_more_deposit_not_item_available(self, api_client, user_buyer):
        product = baker.make(Product, cost=10, amount_available=0)
        data = {
            "product": product.id,
            "amount": 1
        }

        client = api_client()
        user_buyer.deposit = 195
        user_buyer.save()
        client.force_authenticate(user=user_buyer)
        response = client.post(self.endpoint, data=data)
        assert response.status_code == 400
