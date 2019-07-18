"""
# TODO: Update test case description
"""
from django_swagger_utils.utils.test import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from fb_post.models.models import *

REQUEST_BODY = """

"""

RESPONSE_BODY = """
{
    "post_ids": [
        1, 2
    ]
}
"""

TEST_CASE = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "scopes": ["read"], "type": "oauth2"}},
        "body": REQUEST_BODY,
    },
    "response": {
        "status": 201,
        "body": RESPONSE_BODY,
        "header_params": {}
    }
}


class TestCase01GetPositivePostsAPITestCase(CustomAPITestCase):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE

    def setupUser(self, username, password):
        pass

    def setup_user_data(self):
        self.foo_user = self._create_user("user1", "password1")
        self.user_2 = self._create_user("user2", "password2")
        self.user_3 = self._create_user("user2", "password2")
        self.user_4 = self._create_user("user2", "password2")
        self.user_5 = self._create_user("user2", "password2")

    def setup_data(self):
        self.setup_user_data()
        self.post_1 = Post.objects.create(user=self.foo_user, postBody="This is first post")
        self.post_2 = Post.objects.create(user=self.foo_user, postBody="This is second post")
        self.post_3 = Post.objects.create(user=self.foo_user, postBody="This is third post")
        self.post_reaction_1 = PostReactions.objects.create(post=self.post_1, user=self.foo_user, reactionType="LOVE")
        self.post_reaction_2 = PostReactions.objects.create(post=self.post_1, user=self.user_2, reactionType="LIKE")
        self.post_reaction_3 = PostReactions.objects.create(post=self.post_2, user=self.user_3, reactionType="LOVE")


    def test_case(self):
        self.setup_data()
        self.default_test_case()

    # def compareResponse(self, response, test_case_response_dict):
    #
    #     import json
    #     response_data = json.loads(response.content)
    #
    #     post_ids = response_data["post_ids"]
    #
    #     assert self.post_1.id in post_ids
    #     assert self.post_2.id in post_ids
    #     assert response.status_code == 201
