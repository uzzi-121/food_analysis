def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "CookCast AI"


def test_extract_ingredients_endpoint(client):
    response = client.post(
        "/api/v1/ingredients/extract",
        data={"text_input": "김치, 스팸, 계란"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["ingredients"]) >= 3
    assert data["detected_count"] >= 3


def test_recommend_recipes_endpoint(client):
    response = client.post(
        "/api/v1/recipes/recommend",
        json={"ingredients": ["김치", "스팸", "대파"]}
    )
    assert response.status_code == 200
    candidates = response.json()
    assert len(candidates) >= 1
    assert any("김치" in c["title"] for c in candidates)


def test_synthesize_recipe_endpoint(client):
    response = client.post(
        "/api/v1/recipes/synthesize",
        json={
            "recipe_id": "spam-kimchi-fried-rice",
            "recipe_title": "스팸 김치볶음밥",
            "available_ingredients": ["김치", "스팸"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "스팸 김치볶음밥"
    assert len(data["steps"]) >= 4
