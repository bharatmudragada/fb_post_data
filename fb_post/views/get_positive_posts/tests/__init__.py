# pylint: disable=wrong-import-position

APP_NAME = "fb_post"
OPERATION_NAME = "get_positive_posts"
REQUEST_METHOD = "get"
URL_SUFFIX = "posts/reactions/positive/"

from .test_case_01 import TestCase01GetPositivePostsAPITestCase

__all__ = [
    "TestCase01GetPositivePostsAPITestCase"
]
