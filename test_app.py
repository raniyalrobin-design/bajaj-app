from app import app
#comment to test pipeline

def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Bajaj Bicycle Store" in response.data


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "UP"
