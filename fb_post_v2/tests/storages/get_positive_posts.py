import pytest
from freezegun import freeze_time

from fb_post_v2.storages.post_storage import PostStorageImpl
from fb_post_v2.models.models import *


class TestGetPositivePosts:

    @pytest.fixture
    def setup_data(self):
        self.user_1 = User.objects.create(username="user_1", profile_pic_url="https://user_1")
        self.post = Post.objects.create(user=self.user_1, post_content="This is new post")
        self.post_2 = Post.objects.create(user=self.user_1, post_content="This is another post")
        self.post_reaction_1 = PostReactions.objects.create(post=self.post, user=self.user_1, reaction_type="LOVE")
        self.post_reaction_2 = PostReactions.objects.create(post=self.post_2, user=self.user_1, reaction_type="SAD")

    @pytest.mark.django_db
    @freeze_time("2019-08-18")
    def test_get_positive_posts_response(self, setup_data):

        post_storage_object = PostStorageImpl()
        post_ids = post_storage_object.get_posts_with_more_positive_reactions()

        assert self.post.id in post_ids
        assert self.post_2.id in post_ids