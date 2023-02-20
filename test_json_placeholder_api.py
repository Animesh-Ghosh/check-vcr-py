import unittest
import vcr
from json_placeholder_api import Post, get_posts, create_post


class TestJSONPlaceholderAPI(unittest.TestCase):
    def test_get_posts(self):
        with vcr.use_cassette('fixtures/cassettes/test_get_posts.yaml') as cassette:
            posts = get_posts()
            self.assertEqual('https://jsonplaceholder.typicode.com/posts', cassette.requests[0].uri)
            self.assertEqual('GET', cassette.requests[0].method)
            self.assertEqual(200, cassette.responses[0]['status']['code'])
            self.assertEqual(list, type(posts))
            post = posts[0]
            self.assertListEqual(['userId', 'id', 'title', 'body'], list(post.keys()))

    def test_create_post(self):
        with vcr.use_cassette('fixtures/cassettes/test_create_post.yaml') as cassette:
            post = Post(title='foo', body='bar', user_id=1)
            response = create_post(post)
            self.assertEqual('https://jsonplaceholder.typicode.com/posts', cassette.requests[0].uri)
            self.assertEqual('POST', cassette.requests[0].method)
            self.assertEqual(201, cassette.responses[0]['status']['code'])
            self.assertTrue(response.ok)
            self.assertEqual(dict, type(response.json()))
            self.assertEqual('foo', response.json()['title'])
            self.assertEqual('bar', response.json()['body'])
            self.assertEqual(1, response.json()['userId'])
