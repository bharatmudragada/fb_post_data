"""
# Reaction to post with same reaction
"""
from django_swagger_utils.utils.test import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from fb_post.models import Post, PostReactions
from django.core.exceptions import ObjectDoesNotExist

REQUEST_BODY = """
{
    "reaction_type": "LOVE"
}
"""

RESPONSE_BODY = """
{
    "status": "reaction added"
}
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
        "body": RESPONSE_BODY,
        "header_params": {}
    }
}


class TestCase03ReactToPostAPITestCase(CustomAPITestCase):
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
        self.reaction = PostReactions.objects.create(post=self.post, user=self.foo_user, reactionType="LOVE")

    def test_case(self):
        self.setup_data()
        TEST_CASE["request"]["path_params"]["post_id"] = self.post.id
        self.count_before_insertion = PostReactions.objects.count()
        self.default_test_case()

    def _assert_snapshots(self, response):
        super(TestCase03ReactToPostAPITestCase, self)._assert_snapshots(response)
        self.assert_match_snapshot(PostReactions.objects.count() - self.count_before_insertion, "count_difference")

    # def compareResponse(self, response, test_case_response_dict):
    #     super(TestCase03ReactToPostAPITestCase, self).compareResponse(response, test_case_response_dict)
    #
    #     with self.assertRaises(ObjectDoesNotExist) as e:
    #         PostReactions.objects.get(post=self.post, user=self.foo_user)
    #
    #     assert PostReactions.objects.count() == self.count_before_insertion - 1