"""
# TODO: Update test case description
"""
from django_swagger_utils.utils.test import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from fb_post.models.models import *
from freezegun import freeze_time

REQUEST_BODY = """

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
        "status": 201,
        "body": "",
        "header_params": {}
    }
}


class TestCase01GetRepliesToCommentAPITestCase(CustomAPITestCase):
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

    @freeze_time("2019-08-18")
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
        TEST_CASE["request"]["path_params"]["comment_id"] = self.comment.id
        self.default_test_case()

    # def compareResponse(self, response, test_case_response_dict):
    #
    #     import json
    #     replies = json.loads(response.content)
    #
    #     reply_ids = [reply['comment_id'] for reply in replies]
    #
    #     assert [self.reply.id, self.reply_2.id] == reply_ids
    #
    #     reply_one_data = None
    #     for reply in replies:
    #         if reply['comment_id'] == self.reply.id:
    #             reply_one_data = reply
    #             break
    #
    #     assert reply_one_data['commenter']['user_id'] == self.foo_user.id
    #     assert reply_one_data['commenter']['name'] == self.foo_user.username
    #     assert reply_one_data['commenter']['profile_pic_url'] == ""
    #     assert reply_one_data['comment_content'] == "This is a reply"
    #
    #     assert len(replies) <= 2

