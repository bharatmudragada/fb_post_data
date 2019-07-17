# pylint: disable=wrong-import-position

APP_NAME = "fb_post"
OPERATION_NAME = "react_to_post"
REQUEST_METHOD = "post"
URL_SUFFIX = "post/{post_id}/reaction/"

from .test_case_01 import TestCase01ReactToPostAPITestCase
from .test_case_02 import TestCase02ReactToPostAPITestCase
from .test_case_03 import TestCase03ReactToPostAPITestCase

__all__ = [
    "TestCase01ReactToPostAPITestCase",
    "TestCase02ReactToPostAPITestCase",
    "TestCase03ReactToPostAPITestCase"
]
