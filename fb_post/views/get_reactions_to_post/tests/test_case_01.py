"""
# TODO: Update test case description
"""
from django_swagger_utils.utils.test import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from fb_post.models.models import PostReactions, Post

REQUEST_BODY = """

"""

RESPONSE_BODY = """
[
    {
        "name": "username",
        "user_id": 1,
        "profile_pic": "",
        "reaction": "LOVE"
    }
]
"""

TEST_CASE = {
    "request": {
        "path_params": {"post_id": "ibgroup"},
        "query_params": {"offset": 0, "limit": 1},
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


class TestCase01GetReactionsToPostAPITestCase(CustomAPITestCase):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE

    def setupUser(self, username, password):
        pass

    def setup_data(self):
        self.foo_user = self._create_user("username", "password")
        self.post = Post.objects.create(user=self.foo_user, postBody="This is a post")
        self.post_reaction_1 = PostReactions.objects.create(post=self.post, user=self.foo_user, reactionType="LOVE")

    def test_case(self):
        self.setup_data()
        TEST_CASE["request"]["path_params"]["post_id"] = self.post.id
        self.default_test_case()

