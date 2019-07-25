import pytest
from freezegun import freeze_time

from fb_post_v2.storages.post_storage import PostStorageImpl
from fb_post_v2.models.models import *


class TestCreatePost:

    @pytest.fixture
    def setup_data(self):
        self.user_1 = User.objects.create(username="user_1", profile_pic_url="https://user_1")

    @pytest.mark.django_db
    @freeze_time("2019-08-18")
    def test_create_post_response(self, setup_data):

        post_storage_object = PostStorageImpl()
        post_dto = post_storage_object.create_post("This is a testing post", self.user_1.id)

        post = Post.objects.get(pk=1)

        assert post_dto.post_id == post.id
        assert post_dto.user_id == self.user_1.id
        assert post_dto.post_content == post.post_content
        assert post_dto.created_time == post.posted_time
