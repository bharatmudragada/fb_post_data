"""
# TODO: Update test case description
"""
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

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

    def __init__(self, *args, **kwargs):
        self.count_before_insertion = 0
        super(TestCase01CreatePostAPITestCase, self).__init__(
            APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, TEST_CASE, *args, **kwargs)

    def test_case(self):
        self.count_before_insertion = Post.objects.count()
        super(TestCase01CreatePostAPITestCase, self).test_case()

    def compareResponse(self, response, test_case_response_dict):
        super(TestCase01CreatePostAPITestCase, self).compareResponse(response, test_case_response_dict)

        user = self.foo_user
        response_data = json.loads(response.content)
        post_id = response_data["post_id"]

        post = Post.objects.get(pk=post_id)

        assert Post.objects.count() == self.count_before_insertion + 1
        assert post.user_id == post.user_id
        assert post.postBody == "This is a new post"
