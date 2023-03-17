import unittest
import toml
import vcr
from json_placeholder_api import Post, get_posts, create_post


class TOMLSerializer:
    def serialize(self, cassette_dict):
        return toml.dumps(cassette_dict)

    def deserialize(self, cassette_string):
        cassette_dict = toml.loads(cassette_string)
        if 'body' not in cassette_dict['interactions'][0]['request']:
            # TOML does NOT have a concept of null
            cassette_dict['interactions'][0]['request']['body'] = None
        if isinstance(cassette_dict['interactions'][0]['response']['body']['string'], list):
            # TOML seems to store bytes object as a array
            cassette_dict['interactions'][0]['response']['body']['string'] = bytes(cassette_dict['interactions'][0]['response']['body']['string'])
        return cassette_dict


class TestJSONPlaceholderAPI(unittest.TestCase):
    def setUp(self):
        self.vcr = vcr.VCR()
        self.vcr.register_serializer('toml', TOMLSerializer())

    def test_get_posts(self):
        with self.vcr.use_cassette('fixtures/cassettes/test_get_posts.toml', serializer='toml') as cassette:
            posts = get_posts()
            self.assertEqual('https://jsonplaceholder.typicode.com/posts', cassette.requests[0].uri)
            self.assertEqual('GET', cassette.requests[0].method)
            self.assertEqual(200, cassette.responses[0]['status']['code'])
            self.assertEqual(list, type(posts))
            post = posts[0]
            self.assertListEqual(['userId', 'id', 'title', 'body'], list(post.keys()))

    def test_create_post(self):
        with self.vcr.use_cassette('fixtures/cassettes/test_create_post.toml', serializer='toml') as cassette:
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
