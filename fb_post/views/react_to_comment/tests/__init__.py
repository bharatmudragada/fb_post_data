# pylint: disable=wrong-import-position

APP_NAME = "fb_post"
OPERATION_NAME = "react_to_comment"
REQUEST_METHOD = "post"
URL_SUFFIX = "post/{post_id}/comment/{comment_id}/reaction/"

from .test_case_01 import TestCase01ReactToCommentAPITestCase

__all__ = [
    "TestCase01ReactToCommentAPITestCase"
]
