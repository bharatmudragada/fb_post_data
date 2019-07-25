import pytest
from freezegun import freeze_time

from fb_post_v2.storages.post_storage import PostStorageImpl
from fb_post_v2.models.models import *


class TestGetUserPosts:

    @pytest.fixture
    def setup_data(self):
        self.user_1 = User.objects.create(
            username="user_1", profile_pic_url="https://user_1")
        self.user_2 = User.objects.create(
            username="user_2", profile_pic_url="https://user_2")
        self.post_1 = Post.objects.create(
            user=self.user_1, post_content="This is first post")
        self.post_2 = Post.objects.create(
            user=self.user_1, post_content="This is second post")
        self.post_3 = Post.objects.create(
            user=self.user_2, post_content="This is third post")


    @pytest.mark.django_db
    @freeze_time("2019-08-18")
    def test_get_user_posts_response_of_same_user(self, setup_data):

        post_storage_object = PostStorageImpl()
        user_posts_dto = post_storage_object.get_user_posts(
            user_id=self.user_1.id, offset=0, length=2)

        post_ids = [post.post_details.post_id for post in user_posts_dto]

        assert self.post_1.id in post_ids
        assert self.post_2.id in post_ids

    @pytest.mark.django_db
    @freeze_time("2019-08-18")
    def test_get_user_posts_response_of_different_user(self, setup_data):
        post_storage_object = PostStorageImpl()
        user_posts_dto = post_storage_object.get_user_posts(
            user_id=self.user_1.id, offset=0, length=2)

        post_ids = [post.post_details.post_id for post in user_posts_dto]

        assert self.post_3.id not in post_ids

    @pytest.mark.django_db
    @freeze_time("2019-08-18")
    def test_get_user_posts_response_offset(self, setup_data):
        post_storage_object = PostStorageImpl()
        user_posts_dto = post_storage_object.get_user_posts(
            user_id=self.user_1.id, offset=1, length=2)

        post_ids = [post.post_details.post_id for post in user_posts_dto]

        assert self.post_1.id not in post_ids
        assert self.post_2.id in post_ids

    @pytest.mark.django_db
    @freeze_time("2019-08-18")
    def test_get_user_posts_response_length(self, setup_data):
        post_storage_object = PostStorageImpl()
        user_posts_dto = post_storage_object.get_user_posts(
            user_id=self.user_1.id, offset=0, length=1)

        post_ids = [post.post_details.post_id for post in user_posts_dto]

        assert self.post_1.id in post_ids
        assert self.post_2.id not in post_ids