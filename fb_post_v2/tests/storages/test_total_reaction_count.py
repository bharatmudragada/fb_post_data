import pytest
from freezegun import freeze_time

from fb_post_v2.storages.post_storage import PostStorageImpl
from fb_post_v2.models.models import *


class TestTotalReactionCount:

    @pytest.fixture
    def setup_data(self):
        self.user_1 = User.objects.create(
            username="user_1", profile_pic_url="https://user_1")
        self.user_2 = User.objects.create(
            username="user_2", profile_pic_url="https://user_2")
        self.post = Post.objects.create(
            user=self.user_1, post_content="This is new post")
        self.post_reaction_1 = PostReactions.objects.create(
            post=self.post, user=self.user_1, reaction_type="LOVE")
        self.post_reaction_2 = PostReactions.objects.create(
            post=self.post, user=self.user_2, reaction_type="SAD")

    @pytest.mark.django_db
    @freeze_time("2019-08-18")
    def test_total_reaction_count_response(self, setup_data):

        post_storage_object = PostStorageImpl()
        total_reactions_count = post_storage_object.get_total_reaction_count()

        assert total_reactions_count == 2
