import pytest
from fastapi.testclient import TestClient


def test_list_products_empty(client):
    response = client.get('/products')
    assert response.status_code == 200
    data = response.json()
    assert data['items'] == []
    assert data['total'] == 0



def test_create_product(client):
    response = client.post('/products', json={
        'name': 'Keyboard',
        'description': 'Mechanical keyboard',
        'price_cents': 8900,
        'currency': 'EUR',
        'category': 'tech'
    })
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Keyboard'
    assert data['price_cents'] == 8900
    assert data['is_active'] == True



def test_get_product(client):
    # create a product
    create = client.post('/products', json={
        'name': 'Mouse',
        'description': 'Wireless mouse',
        'price_cents': 2900,
        'currency': 'EUR',
        'category': 'tech'
    })
    product_id = create.json()['id']
    
    #get back product
    response = client.get(f'/products/{product_id}')
    assert response.status_code == 200
    assert response.json()['name'] == 'Mouse'


def test_get_product_not_found(client):
    response = client.get('/products/00000000-0000-0000-0000-000000000000')
    assert response.status_code == 404


def test_update_product(client):
    create = client.post('/products', json={
        'name': 'Keyboard',
        'description': 'Mechanical keyboard',
        'price_cents': 8900,
        'currency': 'EUR',
        'category': 'tech'
    })
    product_id = create.json()['id']

    response = client.patch(f'/products/{product_id}', json={
        'price_cents': 7900
    })
    assert response.status_code == 200
    assert response.json()['price_cents'] == 7900


def test_delete_product(client):
    create = client.post('/products', json={
        'name': 'Keyboard',
        'description': 'Mechanical keyboard',
        'price_cents': 8900,
        'currency': 'EUR',
        'category': 'tech'
    })
    product_id = create.json()['id']

    response = client.delete(f'/products/{product_id}')
    assert response.status_code == 204

    # check that the product is no longer accessible
    response = client.get(f'/products/{product_id}')
    assert response.status_code == 404 