def test_register_and_login(client, auth):
    r = auth["register"]()
    assert r.status_code == 200
    r = auth["login"]()
    assert r.status_code == 200
    assert b"Welcome" in r.data
