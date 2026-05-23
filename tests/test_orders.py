import pytest


@pytest.fixture
async def customer_id(client_auth):
    response = await client_auth.post('/customers', json={
        'email': 'testcustomer@example.com',
        'full_name': 'Test Customer',
    })
    assert response.status_code == 201
    return response.json()['id']


async def test_create_order(client_auth, customer_id):
    response = await client_auth.post('/orders', json={
        'customer_id': customer_id,
        'currency': 'EUR'
    })
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'draft'
    assert data['total_cents'] == 0
    assert data['items'] == []


async def test_add_item_to_order(client_auth, customer_id):
    product = (await client_auth.post('/products', json={
        'name': 'Keyboard',
        'description': 'Mechanical keyboard',
        'price_cents': 8900,
        'currency': 'EUR',
        'category': 'tech',
        'stock_quantity': 10,
    })).json()

    order = (await client_auth.post('/orders', json={
        'customer_id': customer_id,
        'currency': 'EUR'
    })).json()

    response = await client_auth.post(f"/orders/{order['id']}/items", json={
        'product_id': product['id'],
        'quantity': 2
    })
    assert response.status_code == 200
    data = response.json()
    assert data['total_cents'] == 17800
    assert len(data['items']) == 1


async def test_pay_order(client_auth, customer_id):
    product = (await client_auth.post('/products', json={
        'name': 'Keyboard',
        'description': 'Mechanical keyboard',
        'price_cents': 8900,
        'currency': 'EUR',
        'category': 'tech',
        'stock_quantity': 10,
    })).json()

    order = (await client_auth.post('/orders', json={
        'customer_id': customer_id,
        'currency': 'EUR'
    })).json()

    await client_auth.post(f"/orders/{order['id']}/items", json={
        'product_id': product['id'],
        'quantity': 1
    })

    response = await client_auth.post(
        f"/orders/{order['id']}/pay",
        headers={'Idempotency-Key': 'test-pay-001'}
    )
    assert response.status_code == 200
    assert response.json()['status'] == 'paid'


async def test_pay_order_idempotent(client_auth, customer_id):
    product = (await client_auth.post('/products', json={
        'name': 'Keyboard',
        'description': 'Mechanical keyboard',
        'price_cents': 8900,
        'currency': 'EUR',
        'category': 'tech',
        'stock_quantity': 10,
    })).json()

    order = (await client_auth.post('/orders', json={
        'customer_id': customer_id,
        'currency': 'EUR'
    })).json()

    await client_auth.post(f"/orders/{order['id']}/items", json={
        'product_id': product['id'],
        'quantity': 1
    })

    await client_auth.post(
        f"/orders/{order['id']}/pay",
        headers={'Idempotency-Key': 'test-idem-001'}
    )

    response = await client_auth.post(
        f"/orders/{order['id']}/pay",
        headers={'Idempotency-Key': 'test-idem-001'}
    )
    assert response.status_code == 200
    assert response.json()['status'] == 'paid'


async def test_pay_order_empty(client_auth, customer_id):
    order = (await client_auth.post('/orders', json={
        'customer_id': customer_id,
        'currency': 'EUR'
    })).json()

    response = await client_auth.post(
        f"/orders/{order['id']}/pay",
        headers={'Idempotency-Key': 'test-empty-001'}
    )
    assert response.status_code == 400


async def test_remove_item(client_auth, customer_id):
    product = (await client_auth.post('/products', json={
        'name': 'Keyboard',
        'description': 'Mechanical keyboard',
        'price_cents': 8900,
        'currency': 'EUR',
        'category': 'tech',
        'stock_quantity': 10,
    })).json()

    order = (await client_auth.post('/orders', json={
        'customer_id': customer_id,
        'currency': 'EUR'
    })).json()

    updated = (await client_auth.post(f"/orders/{order['id']}/items", json={
        'product_id': product['id'],
        'quantity': 1
    })).json()

    item_id = updated['items'][0]['id']

    response = await client_auth.delete(
        f"/orders/{order['id']}/items/{item_id}"
    )
    assert response.status_code == 200

    order_after = (await client_auth.get(f"/orders/{order['id']}")).json()
    assert order_after['total_cents'] == 0
    assert order_after['items'] == []


async def test_update_order_status(client_auth, customer_id):
    order = (await client_auth.post('/orders', json={
        'customer_id': customer_id,
        'currency': 'EUR'
    })).json()

    response = await client_auth.patch(
        f"/orders/{order['id']}/status",
        json={'status': 'shipped'}
    )
    assert response.status_code == 200
    assert response.json()['status'] == 'shipped'


async def test_update_order_status_not_found(client_auth):
    response = await client_auth.patch(
        '/orders/00000000-0000-0000-0000-000000000000/status',
        json={'status': 'shipped'}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'Order not found'


async def test_get_invoice(client_auth, customer_id):
    product = (await client_auth.post('/products', json={
        'name': 'Keyboard',
        'description': 'Mechanical keyboard',
        'price_cents': 8900,
        'currency': 'EUR',
        'category': 'tech',
        'stock_quantity': 10,
    })).json()

    order = (await client_auth.post('/orders', json={
        'customer_id': customer_id,
        'currency': 'EUR'
    })).json()

    await client_auth.post(f"/orders/{order['id']}/items", json={
        'product_id': product['id'],
        'quantity': 1
    })

    await client_auth.post(
        f"/orders/{order['id']}/pay",
        headers={'Idempotency-Key': 'test-invoice-001'}
    )

    invoices = (await client_auth.get(
        f"/orders/{order['id']}/invoices"
    )).json()
    print('invoices response:', invoices)
    assert len(invoices) == 1
    invoice_id = invoices[0]['id']

    response = await client_auth.get(f'/invoices/{invoice_id}')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == invoice_id
    assert data['total_cents'] == 8900
    assert data['tax'] == 1780


async def test_get_invoice_not_found(client_auth):
    response = await client_auth.get(
        '/invoices/00000000-0000-0000-0000-000000000000'
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'Invoice not found'