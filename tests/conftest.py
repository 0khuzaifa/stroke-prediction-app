import pytest
from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    app = create_app("config.TestConfig")
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth(client):
    def register(username="user", email="user@example.com", password="pass"):
        return client.post("/auth/register", data={
            "username": username,
            "email": email,
            "password": password,
        }, follow_redirects=True)

    def login(username="user", password="pass"):
        return client.post("/auth/login", data={
            "username": username,
            "password": password,
        }, follow_redirects=True)

    return {"register": register, "login": login}
