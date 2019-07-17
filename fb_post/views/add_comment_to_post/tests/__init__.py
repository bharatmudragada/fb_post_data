# pylint: disable=wrong-import-position

APP_NAME = "fb_post"
OPERATION_NAME = "add_comment_to_post"
REQUEST_METHOD = "post"
URL_SUFFIX = "post/{post_id}/comment/"

from .test_case_01 import TestCase01AddCommentToPostAPITestCase
from .test_case_02 import TestCase02AddCommentToPostAPITestCase

__all__ = [
    "TestCase01AddCommentToPostAPITestCase",
    "TestCase02AddCommentToPostAPITestCase"
]
