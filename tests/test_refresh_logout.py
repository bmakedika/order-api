def test_refresh_rotates_refresh_token_and_returns_new_access(client):
    client.post('/auth/register', json={
        'username': 'ruser',
        'email': 'ruser@example.com',
        'password': 'pw',
    })

    login = client.post('/auth/login', json={
        'email': 'ruser@example.com',
        'password': 'pw',
    })
    assert login.status_code == 200
    tokens = login.json()
    old_refresh = tokens['refresh_token']
    old_access = tokens['access_token']

    refreshed = client.post('/auth/refresh', json={
        'refresh_token': old_refresh,
    })
    assert refreshed.status_code == 200
    new_tokens = refreshed.json()

    assert new_tokens['access_token'] != old_access
    assert new_tokens['refresh_token'] != old_refresh

    # Old refresh should now be invalid (rotation)
    again = client.post('/auth/refresh', json={
        'refresh_token': old_refresh,
    })
    assert again.status_code == 401


def test_logout_revokes_refresh_token(client):
    client.post('/auth/register', json={
        'username': 'luser',
        'email': 'luser@example.com',
        'password': 'pw',
    })

    login_response = client.post('/auth/login', json={
        'email': 'luser@example.com',
        'password': 'pw',
    })
    refresh_token = login_response.json()['refresh_token']
    # Log out, which should revoke the refresh token
    out = client.post('/auth/logout', json={
        'refresh_token': refresh_token,
    })
    assert out.status_code == 200
    # After logout, the refresh token should be revoked and not work anymore
    refreshed = client.post('/auth/refresh', json={
        'refresh_token': refresh_token,
    })
    assert refreshed.status_code == 401