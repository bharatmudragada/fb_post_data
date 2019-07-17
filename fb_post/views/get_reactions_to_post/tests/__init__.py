# pylint: disable=wrong-import-position

APP_NAME = "fb_post"
OPERATION_NAME = "get_reactions_to_post"
REQUEST_METHOD = "get"
URL_SUFFIX = "post/{post_id}/reactions/"

from .test_case_01 import TestCase01GetReactionsToPostAPITestCase

__all__ = [
    "TestCase01GetReactionsToPostAPITestCase"
]
