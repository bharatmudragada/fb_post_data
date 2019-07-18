"""
# Reply to reply is also a reply to comment
"""
from django_swagger_utils.utils.test import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from fb_post.models import Post, Comment

REQUEST_BODY = """
{
    "comment_text": "This is reply to reply"
}
"""

RESPONSE_BODY = """
{
    "reply_comment_id": 3
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


class TestCase02AddReplyToCommentAPITestCase(CustomAPITestCase):
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
        self.comment = Comment.objects.create(post=self.post, commented_on=None, user=self.foo_user, commentText="This is a comment")
        self.reply = Comment.objects.create(post=self.post, commented_on=self.comment, user=self.foo_user, commentText="This is a reply")

    def test_case(self):
        self.setup_data()
        TEST_CASE["request"]["path_params"]["post_id"] = self.post.id
        TEST_CASE["request"]["path_params"]["comment_id"] = self.reply.id
        self.default_test_case()

    def _assert_snapshots(self, response):
        super(TestCase02AddReplyToCommentAPITestCase, self)._assert_snapshots(response)

        import json
        response_data = json.loads(response.content)
        reply_to_reply_id = response_data["reply_comment_id"]
        reply = Comment.objects.get(pk=reply_to_reply_id)

        self.assert_match_snapshot(reply.post_id, "post_id")
        self.assert_match_snapshot(reply.commented_on_id, "commented_on_id")
        self.assert_match_snapshot(reply.user_id, "user_id")
        self.assert_match_snapshot(reply.commentText, "comment_text")

    # def compareResponse(self, response, test_case_response_dict):
    #     super(TestCase02AddReplyToCommentAPITestCase, self).compareResponse(response, test_case_response_dict)
    #
    #     import json
    #     response_data = json.loads(response.content)
    #
    #     reply_to_reply_id = response_data["reply_comment_id"]
    #
    #     reply = Comment.objects.get(pk=reply_to_reply_id)
    #
    #     assert reply.post == self.post
    #     assert reply.commented_on.id == self.comment.id
    #     assert reply.user == self.foo_user
    #     assert reply.commentText == "This is reply to reply"

