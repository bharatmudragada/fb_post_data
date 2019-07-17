# pylint: disable=wrong-import-position

APP_NAME = "fb_post"
OPERATION_NAME = "get_post_details"
REQUEST_METHOD = "get"
URL_SUFFIX = "post/{post_id}/"

from .test_case_01 import TestCase01GetPostDetailsAPITestCase

__all__ = [
    "TestCase01GetPostDetailsAPITestCase"
]
