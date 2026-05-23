import pytest

pytestmark = pytest.mark.asyncio


async def test_list_products_empty(client_auth):
    response = await client_auth.get('/products')
    assert response.status_code == 200
    data = response.json()
    assert data['items'] == []
    assert data['total'] == 0


async def test_create_product(client_auth):
    response = await client_auth.post('/products', json={
        'name':        'Keyboard',
        'description': 'Mechanical keyboard',
        'price_cents': 8900,
        'currency':    'EUR',
        'category':    'tech',
    })
    assert response.status_code == 200
    data = response.json()
    assert data['name']       == 'Keyboard'
    assert data['price_cents'] == 8900
    assert data['is_active']  == True
    assert data['stock_quantity']    == 0
    assert data['reserved_quantity'] == 0


async def test_get_product(client_auth):
    create = await client_auth.post('/products', json={
        'name':        'Mouse',
        'description': 'Wireless mouse',
        'price_cents': 2900,
        'currency':    'EUR',
        'category':    'tech',
    })
    product_id = create.json()['id']

    response = await client_auth.get(f'/products/{product_id}')
    assert response.status_code == 200
    assert response.json()['name'] == 'Mouse'


async def test_get_product_not_found(client_auth):
    response = await client_auth.get('/products/00000000-0000-0000-0000-000000000000')
    assert response.status_code == 404


async def test_update_product(client_auth):
    create = await client_auth.post('/products', json={
        'name':        'Keyboard',
        'description': 'Mechanical keyboard',
        'price_cents': 8900,
        'currency':    'EUR',
        'category':    'tech',
    })
    product_id = create.json()['id']

    response = await client_auth.patch(f'/products/{product_id}', json={
        'price_cents': 7900
    })
    assert response.status_code == 200
    assert response.json()['price_cents'] == 7900


async def test_delete_product(client_auth):
    create = await client_auth.post('/products', json={
        'name':        'Keyboard',
        'description': 'Mechanical keyboard',
        'price_cents': 8900,
        'currency':    'EUR',
        'category':    'tech',
    })
    product_id = create.json()['id']

    response = await client_auth.delete(f'/products/{product_id}')
    assert response.status_code == 204

    response = await client_auth.get(f'/products/{product_id}')
    assert response.status_code == 404