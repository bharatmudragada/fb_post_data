"""
# TODO: Update test case description
"""
from django_swagger_utils.utils.test import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

from fb_post.models.models import Post

import json

REQUEST_BODY = """
{
    "post_content": "This is a new post"
}
"""

RESPONSE_BODY = """
{
    "post_id": 1
}
"""

TEST_CASE = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "scopes": ["write"], "type": "oauth2"}},
        "body": REQUEST_BODY,
    },
    "response": {
        "status": 201,
        "body": RESPONSE_BODY,
        "header_params": {}
    }
}


class TestCase01CreatePostAPITestCase(CustomAPITestCase):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE

    def test_case(self):
        self.count_before_insertion = Post.objects.count()
        self.default_test_case()

    def _assert_snapshots(self, response):
        super(TestCase01CreatePostAPITestCase, self)._assert_snapshots(response)
        response_data = json.loads(response.content)
        post_id = response_data["post_id"]
        post = Post.objects.get(pk=post_id)
        self.assert_match_snapshot(Post.objects.count() - self.count_before_insertion, "count_difference")
        self.assert_match_snapshot(post.user_id, "user_id")
        self.assert_match_snapshot(post.postBody, "post_content")

    # def compareResponse(self, response, test_case_response_dict):
    #     super(TestCase01CreatePostAPITestCase, self).compareResponse(response, test_case_response_dict)
    #
    #     user = self.foo_user
    #     response_data = json.loads(response.content)
    #     post_id = response_data["post_id"]
    #
    #     post = Post.objects.get(pk=post_id)
    #
    #     assert Post.objects.count() == self.count_before_insertion + 1
    #     assert post.user_id == post.user_id
    #     assert post.postBody == "This is a new post"
