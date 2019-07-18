"""
# TODO: Update test case description
"""
from django_swagger_utils.utils.test import CustomAPITestCase

from fb_post.models.models import Post, PostReactions
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

REQUEST_BODY = """

"""

TEST_CASE = {
    "request": {
        "path_params": {"post_id": "ibgroup"},
        "query_params": {},
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


class TestCase01GetReactionMetricsAPITestCase(CustomAPITestCase):
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
        self.user_3 = self._create_user("user3", "password3")
        self.user_4 = self._create_user("user4", "password4")
        self.user_5 = self._create_user("user5", "password5")

    def setup_data(self):
        self.setup_user_data()
        self.post_1 = Post.objects.create(user=self.foo_user, postBody="This is first post")
        self.post_2 = Post.objects.create(user=self.foo_user, postBody="This is second post")

        self.post_reaction_1 = PostReactions.objects.create(post=self.post_1, user=self.foo_user, reactionType="LOVE")
        self.post_reaction_2 = PostReactions.objects.create(post=self.post_1, user=self.user_2, reactionType="LIKE")
        self.post_reaction_3 = PostReactions.objects.create(post=self.post_1, user=self.user_3, reactionType="LIKE")
        self.post_reaction_4 = PostReactions.objects.create(post=self.post_1, user=self.user_4, reactionType="SAD")
        self.post_reaction_5 = PostReactions.objects.create(post=self.post_2, user=self.user_4, reactionType="SAD")

    def test_case(self):
        self.setup_data()
        TEST_CASE["request"]["path_params"]["post_id"] = self.post_1.id
        self.default_test_case()