"""
# TODO: Update test case description
"""
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

from fb_post.models import *

REQUEST_BODY = """

"""

TEST_CASE = {
    "request": {
        "path_params": {},
        "query_params": {"offset": 0, "limit": 5},
        "header_params": {},
        "securities": {"oauth": {"tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "scopes": ["read"], "type": "oauth2"}},
        "body": REQUEST_BODY,
    },
    "response": {
        "status": 201,
        "body": "",
        "header_params": {}
    }
}


class TestCase02GetUserPostsAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase02GetUserPostsAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, TEST_CASE, *args, **kwargs)

    def setupUser(self, username, password):
        pass

    def setup_user_data(self):
        self.foo_user = self._create_user("user1", "password1")
        self.user_2 = self._create_user("user2", "password2")

    def setup_data(self):
        self.setup_user_data()
        self.post_1 = Post.objects.create(user=self.foo_user, postBody="This is first post")
        self.post_2 = Post.objects.create(user=self.foo_user, postBody="This is second post")
        self.post_3 = Post.objects.create(user=self.user_2, postBody="This is third post")

    def test_case(self):
        self.setup_data()

        super(TestCase02GetUserPostsAPITestCase, self).test_case()

    def compareResponse(self, response, test_case_response_dict):

        import json
        posts = json.loads(response.content)

        post_ids = []
        for post in posts:
            post_ids.append(post["post_id"])

        assert self.post_3.id not in post_ids
        assert response.status_code == 201
