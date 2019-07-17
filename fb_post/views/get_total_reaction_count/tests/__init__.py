# pylint: disable=wrong-import-position

APP_NAME = "fb_post"
OPERATION_NAME = "get_total_reaction_count"
REQUEST_METHOD = "get"
URL_SUFFIX = "reactions/total_count/"

from .test_case_01 import TestCase01GetTotalReactionCountAPITestCase

__all__ = [
    "TestCase01GetTotalReactionCountAPITestCase"
]
