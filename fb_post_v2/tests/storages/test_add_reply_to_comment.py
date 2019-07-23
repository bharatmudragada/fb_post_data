import pytest
from freezegun import freeze_time

from fb_post_v2.storages.post_storage import PostStorage
from fb_post_v2.models.models import *


class TestAddReplyToComment:

    @pytest.fixture
    def setup_data(self):
        self.user_1 = User.objects.create(username="user_1", profile_pic_url="https://user_1")
        self.post = Post.objects.create(user=self.user_1, post_content="This is new post")
        self.comment = Comment.objects.create(post=self.post, user=self.user_1, commented_on=None, comment_text="This is comment")

    @pytest.mark.django_db
    @freeze_time("2019-08-18")
    def test_add_reply_to_comment_response(self, setup_data):

        post_storage_object = PostStorage()
        reply_dto = post_storage_object.add_reply_to_comment(self.comment.id, self.user_1.id, "This is reply")

        reply = Comment.objects.filter(post_id=self.post.id, commented_on=self.comment).first()

        assert reply_dto.comment_id == reply.id
        assert reply_dto.user_id == reply.user_id
        assert reply_dto.commented_at == reply.commented_time
        assert reply_dto.comment_content == reply.comment_text
        assert reply_dto.commented_on_id == reply.commented_on_id
