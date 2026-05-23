async def test_users_me_require_auth(client):
    response = await client.get('/users/me')
    assert response.status_code in (401, 403)


async def test_users_me_returns_user(client):
    await client.post('/auth/register', json={
        'username': 'meuser',
        'email': 'meuser@exemple.com',
        'password': 'testpassword',
    })
    login = await client.post('/auth/login', json={
        'email': 'meuser@exemple.com',
        'password': 'testpassword'
    })
    token = login.json()['access_token']
    response = await client.get(
        '/users/me',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == 'meuser@exemple.com'
    assert data['username'] == 'meuser'
    assert data['role'] == 'user'