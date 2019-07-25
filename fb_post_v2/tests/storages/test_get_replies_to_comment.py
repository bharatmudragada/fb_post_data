import pytest
from freezegun import freeze_time

from fb_post_v2.storages.post_storage import PostStorageImpl
from fb_post_v2.models.models import *


class TestGetRepliesToComment:

    @pytest.fixture
    def setup_data(self):
        self.user_1 = User.objects.create(username="user_1", profile_pic_url="https://user_1")
        self.user_2 = User.objects.create(username="user_2", profile_pic_url="https://user_2")
        self.post = Post.objects.create(user=self.user_1, post_content="This is new post")
        self.comment = Comment.objects.create(post=self.post, user=self.user_1, commented_on=None, comment_text="This is comment")
        self.reply_1 = Comment.objects.create(post=self.post, user=self.user_1, commented_on=self.comment, comment_text="This is reply one")
        self.reply_2 = Comment.objects.create(post=self.post, user=self.user_1, commented_on=self.comment, comment_text="This is reply two")

    @pytest.mark.django_db
    @freeze_time("2019-08-18")
    def test_get_replies_to_comment_response(self, setup_data):

        post_storage_object = PostStorageImpl()
        replies_dto = post_storage_object.get_comment_replies(self.comment.id, 0, 2)

        reply_ids = [reply.comment_id for reply in replies_dto]

        assert self.reply_1.id in reply_ids
        assert self.reply_2.id in reply_ids

        reply_one_data = None
        for reply in replies_dto:
            if reply.comment_id == self.reply_1.id:
                reply_one_data = reply
                break

        reply_user = reply_one_data.user
        assert reply_user.user_id == self.user_1.id
        assert reply_user.name == self.user_1.username
        assert reply_user.profile_pic_url == self.user_1.profile_pic_url

        assert reply_one_data.commented_at == self.reply_1.commented_time
        assert reply_one_data.comment_content == self.reply_1.comment_text
