import unittest
import vcr
from json_placeholder_api import Post, User, get_posts, get_user_posts, create_post


class TestJSONPlaceholderAPI(unittest.TestCase):
    def setUp(self):
        self.vcr = vcr.VCR(
            match_on=['method', 'scheme', 'host', 'port', 'path', 'query', 'body']
        )

    def test_get_posts(self):
        with self.vcr.use_cassette('fixtures/cassettes/test_get_posts.yaml') as cassette:
            posts = get_posts()
            self.assertEqual('https://jsonplaceholder.typicode.com/posts', cassette.requests[0].uri)
            self.assertEqual('GET', cassette.requests[0].method)
            self.assertEqual(200, cassette.responses[0]['status']['code'])
            self.assertIsInstance(posts, list)
            post = posts[0]
            self.assertListEqual(['userId', 'id', 'title', 'body'], list(post.keys()))

    def test_get_user_posts(self):
        with self.vcr.use_cassette('fixtures/cassettes/test_get_user_posts.yaml', record_mode='new_episodes') as cassette:
            user = User(user_id=2)
            response = get_user_posts(user)
            latest_cassette_index = len(cassette.requests) - 1
            self.assertEqual('https://jsonplaceholder.typicode.com/user/2/posts', cassette.requests[latest_cassette_index].uri)
            self.assertEqual('GET', cassette.requests[latest_cassette_index].method)
            self.assertEqual(200, cassette.responses[latest_cassette_index]['status']['code'])
            self.assertTrue(response.ok)
            self.assertIsInstance(response.json(), list)
            post = response.json()[0]
            self.assertEqual(2, post['userId'])

    def test_create_post(self):
        with self.vcr.use_cassette('fixtures/cassettes/test_create_post.yaml', record_mode='none') as cassette:
            post = Post(title='foo', body='bar', user_id=1)
            response = create_post(post)
            self.assertEqual('https://jsonplaceholder.typicode.com/posts', cassette.requests[0].uri)
            self.assertEqual('POST', cassette.requests[0].method)
            self.assertEqual(201, cassette.responses[0]['status']['code'])
            self.assertTrue(response.ok)
            self.assertIsInstance(response.json(), dict)
            self.assertEqual('foo', response.json()['title'])
            self.assertEqual('bar', response.json()['body'])
            self.assertEqual(1, response.json()['userId'])
