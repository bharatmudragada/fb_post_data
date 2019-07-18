"""
# TODO: Update test case description
"""
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

from fb_post.models.models import Post, PostReactions
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

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


class TestCase02GetReactionMetricsAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase02GetReactionMetricsAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD,
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
        self.setup_user_data()
        self.post_1 = Post.objects.create(user=self.foo_user, postBody="This is first post")


    def test_case(self):
        self.setup_data()
        TEST_CASE["request"]["path_params"]["post_id"] = self.post_1.id
        super(TestCase02GetReactionMetricsAPITestCase, self).test_case()

    def compareResponse(self, response, test_case_response_dict):
        import json
        response_data = json.loads(response.content)

        assert response_data == []