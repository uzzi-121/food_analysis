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


def test_discover_recipes_by_intent_endpoint(client):
    """Test natural language intent discovery endpoint."""
    response = client.post(
        "/api/v1/recipes/discover",
        json={
            "query": "오늘 비 오는데 얼큰한 국물 요리 먹고 싶어",
            "context_ingredients": ["김치", "돼지고기"]
        }
    )
    assert response.status_code == 200
    candidates = response.json()
    assert len(candidates) >= 1
    # Check that best match is soup and has AI reasoning
    assert candidates[0]["id"] == "pork-kimchi-jjigae"
    assert candidates[0]["ai_reasoning"] is not None
    assert candidates[0]["intent_score"] >= 80


def test_dual_input_recipe_discovery_endpoint(client):
    """Test dual input: Refrigerator ingredients + Desired recipe style."""
    response = client.post(
        "/api/v1/recipes/discover",
        json={
            "query": "맥주 안주로 먹을 부드러운 고단백 요리",
            "context_ingredients": ["계란", "대파"]
        }
    )
    assert response.status_code == 200
    candidates = response.json()
    assert len(candidates) >= 1
    assert candidates[0]["id"] == "rolled-omelet"
    assert "계란" in candidates[0]["ai_reasoning"]


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
