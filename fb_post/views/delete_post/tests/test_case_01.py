"""
# TODO: Update test case description
"""
from django_swagger_utils.utils.test import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from fb_post.models.models import *

REQUEST_BODY = """

"""

TEST_CASE = {
    "request": {
        "path_params": {"post_id": "ibgroup"},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "scopes": ["write"], "type": "oauth2"}},
        "body": REQUEST_BODY,
    },
    "response": {
        "status": 201,
        "body": '{"status": "post_deleted"}',
        "header_params": {}
    }
}


class TestCase01DeletePostAPITestCase(CustomAPITestCase):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE

    def setupUser(self, username, password):
        pass

    def setup_data(self):
        self.foo_user = self._create_user('username', 'password')
        self.post = Post.objects.create(user=self.foo_user, postBody="This is comment post")

    def test_case(self):
        self.setup_data()
        TEST_CASE["request"]["path_params"]["post_id"] = self.post.id
        self.count_before_insertion = Post.objects.count()
        self.default_test_case()

    def _assert_snapshots(self, response):
        super(TestCase01DeletePostAPITestCase, self)._assert_snapshots(response)
        self.assert_match_snapshot(Post.objects.count() - self.count_before_insertion, "count_difference")

        from django.core.exceptions import ObjectDoesNotExist
        with self.assertRaises(ObjectDoesNotExist) as e:
            Post.objects.get(pk=self.post.id)

    # def compareResponse(self, response, test_case_response_dict):
    #     super(TestCase01DeletePostAPITestCase, self).compareResponse(response, test_case_response_dict)
    #
    #     assert Post.objects.count() == self.count_before_insertion - 1
    #
    #     from django.core.exceptions import ObjectDoesNotExist
    #     with self.assertRaises(ObjectDoesNotExist) as e:
    #         Post.objects.get(pk=self.post.id)
