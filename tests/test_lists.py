import pytest
from main import app
from unittest.mock import Mock

@pytest.mark.parametrize("list_name", [
"popular",
"top_rated",
"now_playing",
"upcoming"
])
def test_homepage_lists(monkeypatch, list_name):

    api_mock = Mock(return_value=[])

    monkeypatch.setattr("tmdb_client.get_movies", api_mock)

    with app.test_client() as client:
        response = client.get(f"/?list_name={list_name}")

        assert response.status_code == 200

        api_mock.assert_called_once_with(how_many=12, list_type=list_name)