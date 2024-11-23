from json import loads

from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_add_recipe():
    recipe = {
        "name": "Banana Muffins",
        "time": 35,
        "ingredients": f"1 ½ cups all-purpose flour, 1 ½ cups all-purpose flour, "
        f"1 teaspoon baking powder, 1 teaspoon baking soda, ½ teaspoon salt, "
        f"3 ripe bananas, ¾ cup white sugar, 1 egg, ⅓ cup butter, melted",
        "description": f"Gather all ingredients. Preheat the oven to 350 degrees F (175 degrees C). "
        f"Grease a 12-cup muffin tin or line cups with paper liners. "
        f"Sift flour, baking powder, baking soda, and salt together in a bowl; set aside."
        f"Mix bananas, sugar, egg, and melted butter in a separate large bowl until well combined; "
        f"fold in flour mixture until smooth. Spoon batter into the prepared muffin cups, "
        f"filling each 2/3 full. Bake in the preheated oven until tops spring back when "
        f"lightly pressed, about 25 to 30 minutes.",
    }
    response = client.post("/recipes", json=recipe)
    assert response.status_code == 200
    assert loads(response.text) == recipe


def test_get_recipes() -> None:
    response = client.get("/recipes")
    response_json = loads(response.text)
    assert response.status_code == 200
    assert isinstance(response_json, list)
    assert isinstance(response_json[0], dict)


def test_get_recipe():
    response = client.get("/recipes/<int:id>?recipe_id=1")
    assert response.status_code == 200
    assert isinstance(loads(response.text), dict)


def test_get_recipe_failed():
    response = client.get("/recipes/<int:id>?recipe_id=10")
    assert response.status_code == 404
    assert loads(response.text) == {
        "detail": "The server can't find the requested resource"
    }
