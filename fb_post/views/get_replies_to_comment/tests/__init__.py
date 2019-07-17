# pylint: disable=wrong-import-position

APP_NAME = "fb_post"
OPERATION_NAME = "get_replies_to_comment"
REQUEST_METHOD = "get"
URL_SUFFIX = "comment/{comment_id}/replies/"

from .test_case_01 import TestCase01GetRepliesToCommentAPITestCase

__all__ = [
    "TestCase01GetRepliesToCommentAPITestCase"
]
