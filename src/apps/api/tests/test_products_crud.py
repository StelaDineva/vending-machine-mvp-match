import json

import pytest
from model_bakery import baker

from products.models import Product


pytestmark = pytest.mark.django_db


class TestProductCRUDEndpoints:

    endpoint = '/api/products/'

    def test_list_unauthenticated(self, api_client):
        baker.make(Product, _quantity=3)

        response = api_client().get(
            self.endpoint
        )

        assert response.status_code == 401

    def test_list_as_seller(self, api_client, user_seller):
        baker.make(Product, _quantity=3)

        client = api_client()
        client.force_authenticate(user=user_seller)
        response = client.get(
            self.endpoint
        )

        assert response.status_code == 200

    def test_list_as_buyer(self, api_client, user_buyer):
        baker.make(Product, _quantity=3)

        client = api_client()
        client.force_authenticate(user=user_buyer)
        response = client.get(
            self.endpoint
        )

        assert response.status_code == 200

    def test_create_unauthenticated(self, api_client):
        expected_json = {
            'name': "product name",
            'seller_id': "seller id",
            'cost': 10,
            'amount_available': 10
        }

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json'
        )

        assert response.status_code == 401

    def test_create_as_buyer(self, api_client, user_buyer):
        expected_json = {
            'name': "product name",
            'seller_id': "seller id",
            'cost': 10,
            'amount_available': 10
        }

        client = api_client()
        client.force_authenticate(user=user_buyer)
        response = client.post(
            self.endpoint,
            data=expected_json,
            format='json'
        )

        assert response.status_code == 403

    def test_create_as_seller(self, api_client, user_seller):
        expected_json = {
            'name': "product name",
            'seller_id': "seller id",
            'cost': 10,
            'amount_available': 10
        }

        client = api_client()
        client.force_authenticate(user=user_seller)
        response = client.post(
            self.endpoint,
            data=expected_json,
            format='json'
        )

        assert response.status_code == 201
        assert json.loads(response.content) == expected_json

    def test_create_as_seller_not_valid(self, api_client, user_seller):
        expected_json = {
            'name': "product name",
            'seller_id': "seller id",
            'cost': 11,
            'amount_available': 10
        }

        client = api_client()
        client.force_authenticate(user=user_seller)
        response = client.post(
            self.endpoint,
            data=expected_json,
            format='json'
        )

        assert response.status_code == 400
        assert json.loads(response.content)['cost'] == ['11 should be in multiples of 5']

    def test_retrieve_unauthenticated(self, api_client):
        product = baker.make(Product)
        url = f'{self.endpoint}{product.id}/'

        response = api_client().get(url)

        assert response.status_code == 401

    def test_retrieve_seller(self, api_client, user_seller):
        product = baker.make(Product)
        url = f'{self.endpoint}{product.id}/'
        expected_json = {
            'name': product.name,
            'seller_id': product.seller_id,
            'cost': product.cost,
            'amount_available': product.amount_available
        }

        client = api_client()
        client.force_authenticate(user=user_seller)
        response = client.get(url)

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_retrieve_buyer(self, api_client, user_buyer):
        product = baker.make(Product)
        url = f'{self.endpoint}{product.id}/'

        client = api_client()
        client.force_authenticate(user=user_buyer)
        response = client.get(url)

        assert response.status_code == 403

    def test_update(self, api_client):
        old_product = baker.make(Product)
        new_product = baker.prepare(Product)
        product_dict = {
            'name': new_product.name,
            'seller_id': new_product.seller_id,
            'cost': new_product.cost,
            'amount_available': new_product.amount_available
        }

        url = f'{self.endpoint}{old_product.id}/'

        response = api_client().put(
            url,
            product_dict,
            format='json'
        )

        assert response.status_code == 401

    def test_update_buyer(self, api_client, user_buyer):
        old_product = baker.make(Product)
        new_product = baker.prepare(Product)
        product_dict = {
            'name': new_product.name,
            'seller_id': new_product.seller_id,
            'cost': new_product.cost,
            'amount_available': new_product.amount_available
        }

        url = f'{self.endpoint}{old_product.id}/'

        client = api_client()
        client.force_authenticate(user=user_buyer)
        response = client.put(
            url,
            product_dict,
            format='json'
        )

        assert response.status_code == 403

    def test_update_seller(self, api_client, user_seller):
        old_product = baker.make(Product, cost=10)
        new_product = baker.prepare(Product, cost=15)
        product_dict = {
            'name': new_product.name,
            'seller_id': new_product.seller_id,
            'cost': new_product.cost,
            'amount_available': new_product.amount_available
        }

        url = f'{self.endpoint}{old_product.id}/'

        client = api_client()
        client.force_authenticate(user=user_seller)
        response = client.put(
            url,
            product_dict,
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content) == product_dict

    @pytest.mark.parametrize(
        'field',
        ['seller_id', 'name', 'cost', 'amount_available']
    )
    def test_partial_update(self, field, api_client, user_seller):
        product = baker.make(Product, cost=10)
        product_dict = {
            'name': "New name",
            'seller_id': "New seller",
            'cost': 55,
            'amount_available': 10
        }
        valid_field = product_dict[field]
        url = f'{self.endpoint}{product.id}/'

        client = api_client()
        client.force_authenticate(user=user_seller)
        response = client.patch(
            url,
            {field: valid_field},
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)[field] == valid_field

    def test_delete(self, api_client):
        product = baker.make(Product)
        url = f'{self.endpoint}{product.id}/'

        response = api_client().delete(url)

        assert response.status_code == 401
        assert Product.objects.all().count() == 1

    def test_delete_buyer(self, api_client, user_buyer):
        product = baker.make(Product)
        url = f'{self.endpoint}{product.id}/'

        client = api_client()
        client.force_authenticate(user=user_buyer)
        response = client.delete(url)

        assert response.status_code == 403
        assert Product.objects.all().count() == 1

    def test_delete_seller(self, api_client, user_seller):
        product = baker.make(Product)
        url = f'{self.endpoint}{product.id}/'

        client = api_client()
        client.force_authenticate(user=user_seller)
        response = client.delete(url)

        assert response.status_code == 204
        assert Product.objects.all().count() == 0
