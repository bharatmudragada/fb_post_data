# pylint: disable=wrong-import-position

APP_NAME = "fb_post"
OPERATION_NAME = "add_reply_to_comment"
REQUEST_METHOD = "post"
URL_SUFFIX = "post/{post_id}/comment/{comment_id}/reply/"

from .test_case_01 import TestCase01AddReplyToCommentAPITestCase

__all__ = [
    "TestCase01AddReplyToCommentAPITestCase"
]
