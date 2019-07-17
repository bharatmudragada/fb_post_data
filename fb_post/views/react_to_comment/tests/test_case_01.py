"""
# TODO: Update test case description
"""
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from fb_post.models import Post, Comment, CommentReactions

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


class TestCase01ReactToCommentAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01ReactToCommentAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, TEST_CASE, *args, **kwargs)

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
        self.count_before_insertion = CommentReactions.objects.count()
        super(TestCase01ReactToCommentAPITestCase, self).test_case()

    def compareResponse(self, response, test_case_response_dict):
        super(TestCase01ReactToCommentAPITestCase, self).compareResponse(response, test_case_response_dict)

        reaction = CommentReactions.objects.get(comment=self.comment, user=self.foo_user)

        assert CommentReactions.objects.count() == self.count_before_insertion + 1
        assert reaction.reactionType == "LOVE"