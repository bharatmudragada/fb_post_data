# pylint: disable=wrong-import-position

APP_NAME = "fb_post"
OPERATION_NAME = "delete_post"
REQUEST_METHOD = "delete"
URL_SUFFIX = "post/{post_id}/"

from .test_case_01 import TestCase01DeletePostAPITestCase
from .test_case_02 import TestCase02DeletePostAPITestCase

__all__ = [
    "TestCase01DeletePostAPITestCase",
    "TestCase02DeletePostAPITestCase"
]
