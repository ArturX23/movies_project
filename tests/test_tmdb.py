import tmdb_client
from unittest.mock import Mock
import pytest

def test_get_poster_url_uses_default_size():
    """Sprawdza, czy URL plakatu zawiera domyślny rozmiar i ścieżkę."""
    poster_api_path = "/test-path.jpg"

    url = tmdb_client.get_poster_url(poster_path=poster_api_path)

    assert "w342" in url
    assert poster_api_path in url


def test_get_movies_list_type_popular(monkeypatch):
    """Sprawdza, czy get_movies_list poprawnie zwraca listę filmów i używa odpowiedniego endpointa."""

    mock_movies_list = [{"id": 1, "title": "Movie 1"}, {"id": 2, "title": "Movie 2"}]

    # Mockujemy funkcję _get
    def mock_get(endpoint):
        # Sprawdzamy, czy endpoint zawiera 'popular'
        assert "popular" in endpoint
        return {"results": mock_movies_list}

    monkeypatch.setattr(tmdb_client, "_get", mock_get)

    movies = tmdb_client.get_movies_list("popular")
    assert movies == mock_movies_list


def test_get_movies_list_invalid_type():
    """Sprawdza, czy get_movies_list rzuca ValueError dla niepoprawnej listy."""
    with pytest.raises(ValueError):
        tmdb_client.get_movies_list("invalid_list")


def test_get_single_movie(monkeypatch):
    """Sprawdza, czy get_single_movie poprawnie zwraca dane filmu i endpoint API jest użyty."""

    mock_movie = {"id": 101, "title": "Mock Movie"}

    def mock_get(endpoint):
        # Sprawdzamy, czy endpoint zawiera movie_id
        assert "101" in endpoint
        return mock_movie

    monkeypatch.setattr(tmdb_client, "_get", mock_get)

    movie = tmdb_client.get_single_movie(101)
    assert movie["id"] == 101
    assert movie["title"] == "Mock Movie"


def test_get_single_movie_cast(monkeypatch):
    """Sprawdza, czy get_single_movie_cast zwraca listę aktorów i obsługuje limit."""

    # Mock odpowiedzi requests.get
    class MockResponse:
        status_code = 200
        def json(self):
            return {
                "cast": [
                    {"name": "Actor 1"},
                    {"name": "Actor 2"},
                    {"name": "Actor 3"},
                    {"name": "Actor 4"},
                ]
            }

    def mock_requests_get(endpoint, headers):
        # Sprawdzamy, czy endpoint zawiera movie_id
        assert "101" in endpoint
        return MockResponse()

    monkeypatch.setattr(tmdb_client.requests, "get", mock_requests_get)

    cast = tmdb_client.get_single_movie_cast(101, limit=3)
    assert isinstance(cast, list)
    assert len(cast) == 3
    assert cast[0]["name"] == "Actor 1"
    assert cast[-1]["name"] == "Actor 3"