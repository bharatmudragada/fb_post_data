"""
# TODO: Update test case description
"""
from django_swagger_utils.utils.test import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from fb_post.models import Post, Comment

REQUEST_BODY = """
{
    "comment_text": "This is comment to post"
}
"""

RESPONSE_BODY = """
{
    "comment_id": 4
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


class TestCase02AddCommentToPostAPITestCase(CustomAPITestCase):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE

    def setupUser(self, username, password):
        pass

    def setup_data(self):
        self.foo_user = self._create_user('username', 'password')
        self.post = Post.objects.create(user=self.foo_user, postBody="This is comment post")
        Comment.objects.create(post=self.post, commented_on=None, user=self.foo_user, commentText="This is first comment")
        Comment.objects.create(post=self.post, commented_on=None, user=self.foo_user, commentText="This is second comment")
        Comment.objects.create(post=self.post, commented_on=None, user=self.foo_user, commentText="This is third comment")

    def test_case(self):
        self.setup_data()
        TEST_CASE["request"]["path_params"]["post_id"] = self.post.id
        self.count_before_insertion = Comment.objects.filter(post=self.post).count()
        self.default_test_case()

    def _assert_snapshots(self, response):
        super(TestCase02AddCommentToPostAPITestCase, self)._assert_snapshots(response)
        import json
        response_data = json.loads(response.content)
        comment_id = response_data["comment_id"]

        comment = Comment.objects.get(pk=comment_id)

        self.assert_match_snapshot(Comment.objects.filter(post=self.post).count() - self.count_before_insertion, "count_difference")
        self.assert_match_snapshot(comment.user_id, "user_id")
        self.assert_match_snapshot(comment.commentText, "comment_text")
        self.assert_match_snapshot(comment.post_id, "post_id")



    # def compareResponse(self, response, test_case_response_dict):
    #     super(TestCase02AddCommentToPostAPITestCase, self).compareResponse(response, test_case_response_dict)
    #
    #     import json
    #     response_data = json.loads(response.content)
    #     comment_id = response_data["comment_id"]
    #
    #     comment = Comment.objects.get(pk=comment_id)
    #
    #     assert Comment.objects.filter(post=self.post).count() == self.count_before_insertion + 1
    #     assert comment.user_id == self.foo_user.id
    #     assert comment.commentText == "This is comment to post"
    #     assert comment.post_id == self.post.id
