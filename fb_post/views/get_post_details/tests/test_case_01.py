"""
# TODO: Update test case description
"""
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from fb_post.models.models import *

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


class TestCase01GetPostDetailsAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01GetPostDetailsAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX,
                                                                TEST_CASE, *args, **kwargs)

    def setupUser(self, username, password):
        pass

    def setup_user_data(self):
        self.foo_user = self._create_user("user1", "password1")
        self.user_2 = self._create_user("user2", "password2")
        self.user_3 = self._create_user("user3", "password3")
        self.user_4 = self._create_user("user4", "password4")
        self.user_5 = self._create_user("user5", "password5")

    def setup_comment_data(self):
        self.comment = Comment.objects.create(post=self.post, commented_on=None, user=self.foo_user, commentText="This is comment")
        self.reply = Comment.objects.create(post=self.post, commented_on=self.comment, user=self.foo_user, commentText="This is reply")
        self.comment_reaction = CommentReactions.objects.create(comment=self.comment, user=self.user_2, reactionType="LOVE")
        self.comment_reaction_2 = CommentReactions.objects.create(comment=self.comment, user=self.user_3, reactionType="LOVE")
        self.comment_reaction_3 = CommentReactions.objects.create(comment=self.comment, user=self.user_4, reactionType="WOW")

    def setup_data(self):
        self.setup_user_data()
        self.post = Post.objects.create(user=self.foo_user, postBody="This is first post")
        self.post_reaction_1 = PostReactions.objects.create(post=self.post, user=self.user_2, reactionType="WOW")
        self.post_reaction_2 = PostReactions.objects.create(post=self.post, user=self.user_3, reactionType="WOW")
        self.setup_comment_data()

    def test_case(self):
        self.setup_data()
        TEST_CASE["request"]["path_params"]["post_id"] = self.post.id

        super(TestCase01GetPostDetailsAPITestCase, self).test_case()

    def compareResponse(self, response, test_case_response_dict):
        import json
        post_data = json.loads(response.content)

        assert post_data["post_id"] == self.post.id
        assert post_data["posted_by"]["user_id"] == self.foo_user.id
        assert post_data["post_content"] == self.post.postBody
        assert post_data["reactions"]["count"] == 2
        assert post_data["reactions"]["type"].sort() == ["WOW"].sort()

        comments = post_data["comments"]

        comment_ids = [comment["comment_id"] for comment in comments]

        assert self.comment.id in comment_ids

        comment_data = None
        for comment_details in post_data["comments"]:
            if comment_details["comment_id"] == self.comment.id:
                comment_data = comment_details

        assert comment_data["commenter"]["user_id"] == self.foo_user.id
        assert comment_data["comment_content"] == self.comment.commentText
        assert comment_data["commented_at"] == self.comment.commentedTime.strftime('%y-%m-%d %H:%M:%S.%f')

        reply_ids = [reply["comment_id"] for reply in comment_data["replies"]]

        assert self.reply.id in reply_ids

        reply_data = None
        for reply_details in comment_data["replies"]:
            if reply_details["comment_id"] == self.reply.id:
                reply_data = reply_details
                break

        assert reply_data["commenter"]["user_id"] == self.foo_user.id
        assert reply_data["comment_content"] == self.reply.commentText

        assert response.status_code == 201
