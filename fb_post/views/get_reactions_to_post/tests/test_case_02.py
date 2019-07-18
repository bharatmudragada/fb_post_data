"""
# TODO: Update test case description
"""
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

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


class TestCase02GetReactionsToPostAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase02GetReactionsToPostAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, TEST_CASE, *args, **kwargs)

    def setupUser(self, username, password):
        pass

    def setup_data(self):
        self.foo_user = self._create_user("username", "password")
        self.post = Post.objects.create(user=self.foo_user, postBody="This is a post")
        self.post_2 = Post.objects.create(user=self.foo_user, postBody="This is second post")

        self.post_reaction_1 = PostReactions.objects.create(post=self.post_2, user=self.foo_user, reactionType="LOVE")

    def test_case(self):
        self.setup_data()
        TEST_CASE["request"]["path_params"]["post_id"] = self.post.id
        super(TestCase02GetReactionsToPostAPITestCase, self).test_case()

    def compareResponse(self, response, test_case_response_dict):

        import json
        reactions = json.loads(response.content)

        user_ids = [reaction['user_id'] for reaction in reactions]

        assert self.foo_user.id not in user_ids

        assert response.status_code == 201

