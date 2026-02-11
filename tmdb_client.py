import requests

def get_popular_movies():
    endpoint = "https://api.themoviedb.org/3/movie/popular"
    api_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMzU4MDM0ZjNjNWE0NTBhMzMwMmM3YzA3ZTVkZWIxYiIsIm5iZiI6MTc3MDY0MzMyOS44NzYsInN1YiI6IjY5ODlkZjgxNGNmNTRlYjY3YThlNzQyZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.i75Zkcc9D63s2rzW3Hu3GqguF7WtxuxgfCnqo-OUsuE"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()

def get_poster_url(poster_api_path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"

def get_movies(how_many):
    data = get_popular_movies()
    return data["results"][:how_many]