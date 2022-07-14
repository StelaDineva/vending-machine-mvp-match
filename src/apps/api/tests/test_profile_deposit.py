import json

import pytest


pytestmark = pytest.mark.django_db


class TestProductCRUDEndpoints:

    endpoint = '/api/users/deposit/'

    def test_deposit_unauthenticated(self, api_client):
        data = {
            "amount": 10
        }
        response = api_client().post(
            self.endpoint, data
        )
        assert response.status_code == 401

    def test_deposit_seller(self, api_client, user_seller):
        data = {
            "amount": 10
        }

        client = api_client()
        client.force_authenticate(user=user_seller)
        response = client.post(
            self.endpoint, data
        )
        assert response.status_code == 403

    def test_deposit_buyer(self, api_client, user_buyer):
        data = {
            "amount": 10
        }

        user_buyer.deposit = 0
        user_buyer.save()

        client = api_client()
        client.force_authenticate(user=user_buyer)
        response = client.post(
            self.endpoint, data
        )
        assert response.status_code == 200
        assert json.loads(response.content)['deposit'] == data['amount']

    def test_deposit_buyer_with_existing_deposit(self, api_client, user_buyer):
        data = {
            "amount": 10
        }

        user_buyer.deposit = 10
        user_buyer.save()

        client = api_client()
        client.force_authenticate(user=user_buyer)
        response = client.post(
            self.endpoint, data
        )
        assert response.status_code == 200
        assert json.loads(response.content)['deposit'] == 20

    def test_deposit_buyer_with_negative_amount(self, api_client, user_buyer):
        data = {
            "amount": -10
        }

        user_buyer.deposit = 10
        user_buyer.save()

        client = api_client()
        client.force_authenticate(user=user_buyer)
        response = client.post(
            self.endpoint, data
        )

        assert response.status_code == 400
