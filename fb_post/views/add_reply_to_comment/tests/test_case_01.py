"""
# Reply to comment
"""
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from fb_post.models import Post, Comment

REQUEST_BODY = """
{
    "comment_text": "This is reply"
}
"""

RESPONSE_BODY = """
{
    "reply_comment_id": 2
}
"""

TEST_CASE = {
    "request": {
        "path_params": {"post_id": "ibgroup", "comment_id": "ibgroup"},
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


class TestCase01AddReplyToCommentAPITestCase(CustomAPITestCase):

    def __init__(self, *args, **kwargs):
        super(TestCase01AddReplyToCommentAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, TEST_CASE, *args, **kwargs)

    def setupUser(self, username, password):
        pass

    def setup_data(self):
        self.foo_user = self._create_user("username", "password")
        self.post = Post.objects.create(user=self.foo_user, postBody="This is a post")
        self.comment = Comment.objects.create(post=self.post, commented_on=None, user=self.foo_user, commentText="This is a comment")

    def test_case(self):
        self.setup_data()
        TEST_CASE["request"]["path_params"]["post_id"] = self.post.id
        TEST_CASE["request"]["path_params"]["comment_id"] = self.comment.id
        super(TestCase01AddReplyToCommentAPITestCase, self).test_case()

    def compareResponse(self, response, test_case_response_dict):
        super(TestCase01AddReplyToCommentAPITestCase, self).compareResponse(response, test_case_response_dict)

        import json
        response_data = json.loads(response.content)

        reply_id = response_data["reply_comment_id"]

        reply = Comment.objects.get(pk=reply_id)

        assert reply.post == self.post
        assert reply.commented_on.id == self.comment.id
        assert reply.user == self.foo_user
        assert reply.commentText == "This is reply"

