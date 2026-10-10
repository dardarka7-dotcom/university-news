import pytest

from app import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_homepage_shows_news(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Университетские" in response.get_data(as_text=True)
    assert "Студенты представили проекты на научной неделе" in response.get_data(as_text=True)


def test_article_page_shows_full_article(client):
    response = client.get("/news/1")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Студенты представили проекты на научной неделе" in page
    assert "научная неделя" in page


def test_unknown_article_returns_404(client):
    response = client.get("/news/999")

    assert response.status_code == 404


def test_category_filter_shows_matching_news(client):
    response = client.get("/?category=Спорт")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Университетская команда заняла призовое место" in page
    assert "Студенты представили проекты на научной неделе" not in page
