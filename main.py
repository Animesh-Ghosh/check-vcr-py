#!/usr/bin/env python
from json_placeholder_api import Post, get_posts, create_post


def main():
    post = Post(title='foo', body='bar', user_id=1)
    response = create_post(post)
    print(response.ok)
    print(response.json())


if __name__ == '__main__':
    main()
