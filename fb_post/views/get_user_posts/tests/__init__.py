# pylint: disable=wrong-import-position

APP_NAME = "fb_post"
OPERATION_NAME = "get_user_posts"
REQUEST_METHOD = "get"
URL_SUFFIX = "posts/user/"

from .test_case_01 import TestCase01GetUserPostsAPITestCase
from .test_case_02 import TestCase02GetUserPostsAPITestCase

__all__ = [
    "TestCase01GetUserPostsAPITestCase",
    "TestCase02GetUserPostsAPITestCase"
]
