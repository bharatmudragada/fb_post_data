"""
# TODO: Update test case description
"""
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from fb_post.models import Post, PostReactions

REQUEST_BODY = """

"""

RESPONSE_BODY = """
{
    "post_ids": [
        1, 2, 3
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


class TestCase02GetPostsReactedByUserAPITestCase(CustomAPITestCase):
    
    def __init__(self, *args, **kwargs):
        super(TestCase02GetPostsReactedByUserAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD,
                                                                    URL_SUFFIX, TEST_CASE, *args, **kwargs)

    def setupUser(self, username, password):
        pass

    def setup_data(self):
        self.foo_user = self._create_user('username', 'password')
        self.user_2 = self._create_user('username2', 'password2')
        self.post = Post.objects.create(user=self.foo_user, postBody="This is comment post")
        self.post_2 = Post.objects.create(user=self.foo_user, postBody="This is second post")
        self.post_3 = Post.objects.create(user=self.foo_user, postBody="This is third post")
        self.post_4 = Post.objects.create(user=self.user_2, postBody="This is fourth post")
        self.post_reaction_1 = PostReactions.objects.create(post=self.post, user=self.foo_user, reactionType="LOVE")
        self.post_reaction_2 = PostReactions.objects.create(post=self.post_2, user=self.foo_user, reactionType="LIKE")
        self.post_reaction_3 = PostReactions.objects.create(post=self.post_3, user=self.foo_user, reactionType="LOVE")
        self.post_reaction_4 = PostReactions.objects.create(post=self.post_4, user=self.user_2, reactionType="LOVE")

    def test_case(self):
        self.setup_data()
        super(TestCase02GetPostsReactedByUserAPITestCase, self).test_case()

    def compareResponse(self, response, test_case_response_dict):
        super(TestCase02GetPostsReactedByUserAPITestCase, self).compareResponse(response, test_case_response_dict)

        import json
        response_data = json.loads(response.content)

        post_ids = response_data["post_ids"]

        assert self.post_4.id not in post_ids
