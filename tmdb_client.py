import requests

API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMzU4MDM0ZjNjNWE0NTBhMzMwMmM3YzA3ZTVkZWIxYiIsIm5iZiI6MTc3MDY0MzMyOS44NzYsInN1YiI6IjY5ODlkZjgxNGNmNTRlYjY3YThlNzQyZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.i75Zkcc9D63s2rzW3Hu3GqguF7WtxuxgfCnqo-OUsuE"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "accept": "application/json"
}


def _get(endpoint):
    response = requests.get(endpoint, headers=HEADERS)

    if response.status_code != 200:
        print("TMDB ERROR:", response.status_code, response.text)
        return None

    return response.json()


def get_popular_movies():
    endpoint = "https://api.themoviedb.org/3/movie/popular"
    return _get(endpoint)



def get_movies(how_many=12, list_type="popular"):
    return get_movies_list(list_type, how_many)


def get_single_movie(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}"
    return _get(endpoint)


def get_poster_url(poster_path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}{poster_path}"

def get_single_movie_cast(movie_id, limit=12):
    """
    Zwraca listę aktorów w filmie TMDB o podanym movie_id
    limit: ile aktorów zwrócić (domyślnie 12)
    """
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    response = requests.get(endpoint, headers=HEADERS)

    if response.status_code != 200:
        print("TMDB ERROR (cast):", response.status_code, response.text)
        return []

    data = response.json()
    return data.get("cast", [])[:limit]

LIST_TYPES = ["popular", "top_rated", "now_playing", "upcoming"]

def get_movies_list(list_name, how_many=12):
    if list_name not in LIST_TYPES:
        raise ValueError(f"Niepoprawna lista: {list_name}")

    endpoint = f"https://api.themoviedb.org/3/movie/{list_name}"
    data = _get(endpoint)

    if not data:
        return []

    return data.get("results", [])[:how_many]
