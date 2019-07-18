"""
# TODO: Update test case description
"""
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from fb_post.models.models import *
from django_swagger_utils.drf_server.exceptions import BadRequest

REQUEST_BODY = """

"""

RESPONSE_BODY = """
{"response": "Invalid comment id", "http_status_code": 400, "res_status": "INVALID_COMMENT_ID"}
"""

TEST_CASE = {
    "request": {
        "path_params": {"comment_id": "ibgroup"},
        "query_params": {"offset": 0, "limit": 2},
        "header_params": {},
        "securities": {"oauth": {"tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "scopes": ["read"], "type": "oauth2"}},
        "body": REQUEST_BODY,
    },
    "response": {
        "status": 400,
        "body": RESPONSE_BODY,
        "header_params": {}
    }
}


class TestCase02GetRepliesToCommentAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase02GetRepliesToCommentAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD,
                                                                         URL_SUFFIX, TEST_CASE, *args, **kwargs)

    def setupUser(self, username, password):
        pass

    def setup_user_data(self):
        self.foo_user = self._create_user("user1", "password1")
        self.user_2 = self._create_user("user2", "password2")
        self.user_3 = self._create_user("user3", "password3")
        self.user_4 = self._create_user("user4", "password4")
        self.user_5 = self._create_user("user5", "password5")

    def setup_data(self):
        self.foo_user = self._create_user("username", "password")
        self.post = Post.objects.create(user=self.foo_user, postBody="This is a post")
        self.comment = Comment.objects.create(post=self.post, commented_on=None, user=self.foo_user, commentText="This is a comment")
        self.reply = Comment.objects.create(post=self.post, commented_on=self.comment, user=self.foo_user, commentText="This is a reply")
        self.reply_2 = Comment.objects.create(post=self.post, commented_on=self.comment, user=self.foo_user, commentText="This is a 2 reply")
        self.reply_3 = Comment.objects.create(post=self.post, commented_on=self.comment, user=self.foo_user, commentText="This is a 3 reply")

    def test_case(self):
        self.setup_data()
        TEST_CASE["request"]["path_params"]["post_id"] = self.post.id
        TEST_CASE["request"]["path_params"]["comment_id"] = self.reply.id
        super(TestCase02GetRepliesToCommentAPITestCase, self).test_case()

