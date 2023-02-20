import requests

BASE_JSON_PLACEHOLDER_API_URL = 'https://jsonplaceholder.typicode.com'


class Post:
    def __init__(self, title, body, user_id):
        self.title, self.body, self.user_id = title, body, user_id


def get_posts():
    response = requests.get(f'{BASE_JSON_PLACEHOLDER_API_URL}/posts')
    return response.json()


def create_post(post):
    response = requests.post(f'{BASE_JSON_PLACEHOLDER_API_URL}/posts', json={
        'title': post.title,
        'body': post.body,
        'userId': post.user_id
    })
    return response
