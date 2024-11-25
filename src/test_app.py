from json import loads

from fastapi.testclient import TestClient
import pytest

from main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_add_recipe(client):
    data = {
        "name": "apple pie",
        "time": 90,
        "ingredients": "pie crust, apples, sugar, flour, cinnamon, eggs",
        "description": "Make the filling. Assemble the pie. Bake the pie.",
    }
    response = client.post("/recipes", json=data)
    assert response.status_code == 200
    assert loads(response.text) == data


def test_get_recipes(client) -> None:
    response = client.get("/recipes")
    response_json = loads(response.text)
    assert response.status_code == 200
    assert isinstance(response_json, list)
    assert isinstance(response_json[0], dict)


def test_get_recipe(client):
    response = client.get("/recipes/<int:id>?rec_id=1")
    assert response.status_code == 200
    assert isinstance(loads(response.text), dict)


def test_get_recipe_failed(client):
    response = client.get("/recipes/<int:id>?rec_id=10")
    response_json = loads(response.text)
    assert response.status_code == 404
    assert isinstance(response_json, dict)
    assert response_json["detail"] == "The requested resource is not available"
