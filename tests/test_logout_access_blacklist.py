async def test_logout_revokes_access_token_via_blacklist(client):
    await client.post('/auth/register', json={
        'username': 'blkuser',
        'email': 'blkuser@example.com',
        'password': 'pw',
    })
    login = await client.post('/auth/login', json={
        'email': 'blkuser@example.com',
        'password': 'pw'
    })
    access = login.json()['access_token']

    ok = await client.get(
        '/users/me',
        headers={'Authorization': f'Bearer {access}'}
    )
    assert ok.status_code == 200

    out = await client.post(
        '/auth/logout',
        headers={'Authorization': f'Bearer {access}'}
    )
    assert out.status_code == 200

    denied = await client.get(
        '/users/me',
        headers={'Authorization': f'Bearer {access}'}
    )
    assert denied.status_code == 401