"""
# Reaction to post with same reaction
"""
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

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
    def __init__(self, *args, **kwargs):
        super(TestCase03ReactToPostAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, TEST_CASE, *args, **kwargs)

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
        super(TestCase03ReactToPostAPITestCase, self).test_case()

    def compareResponse(self, response, test_case_response_dict):
        super(TestCase03ReactToPostAPITestCase, self).compareResponse(response, test_case_response_dict)

        with self.assertRaises(ObjectDoesNotExist) as e:
            PostReactions.objects.get(post=self.post, user=self.foo_user)

        assert PostReactions.objects.count() == self.count_before_insertion - 1