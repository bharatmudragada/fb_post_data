import pytest
from freezegun import freeze_time

from fb_post_v2.storages.post_storage import PostStorageImpl
from fb_post_v2.models.models import *


class TestAddCommentToPost:

    @pytest.fixture
    def setup_data(self):
        self.user_1 = User.objects.create(username="user_1",
                                          profile_pic_url="https://user_1")
        self.post = Post.objects.create(user=self.user_1,
                                        post_content="This is new post")

    @pytest.mark.django_db
    @freeze_time("2019-08-18")
    def test_add_comment_to_post_response(self, setup_data):

        post_storage_object = PostStorageImpl()
        comment_dto = post_storage_object.add_comment_to_post(
            self.post.id, self.user_1.id, "This is comment")

        comment = Comment.objects.filter(post_id=self.post.id).first()

        assert comment_dto.comment_id == comment.id
        assert comment_dto.user_id == comment.user_id
        assert comment_dto.commented_at == comment.commented_time
        assert comment_dto.comment_content == comment.comment_text
        assert comment_dto.commented_on_id == comment.commented_on_id
