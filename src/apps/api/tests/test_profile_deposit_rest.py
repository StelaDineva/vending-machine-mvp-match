import pytest


pytestmark = pytest.mark.django_db


class TestProductCRUDEndpoints:

    endpoint = '/api/users/reset/'

    def test_deposit_unauthenticated(self, api_client):
        response = api_client().get(
            self.endpoint
        )
        assert response.status_code == 401

    def test_deposit_seller(self, api_client, user_seller):
        client = api_client()
        client.force_authenticate(user=user_seller)
        response = client.get(
            self.endpoint
        )
        assert response.status_code == 403

    def test_deposit_buyer(self, api_client, user_buyer):
        user_buyer.deposit = 10
        user_buyer.save()

        client = api_client()
        client.force_authenticate(user=user_buyer)
        response = client.get(
            self.endpoint
        )
        assert response.status_code == 200
        assert user_buyer.deposit == 0
