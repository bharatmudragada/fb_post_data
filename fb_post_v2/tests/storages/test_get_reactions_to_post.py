import pytest
from freezegun import freeze_time

from fb_post_v2.storages.post_storage import PostStorageImpl
from fb_post_v2.models.models import *


class TestGetReactionsToPost:

    @pytest.fixture
    def setup_data(self):
        self.user_1 = User.objects.create(username="user_1", profile_pic_url="https://user_1")
        self.user_2 = User.objects.create(username="user_2", profile_pic_url="https://user_2")
        self.post = Post.objects.create(user=self.user_1, post_content="This is new post")
        self.post_reaction_1 = PostReactions.objects.create(post=self.post, user=self.user_1, reaction_type="LOVE")
        self.post_reaction_2 = PostReactions.objects.create(post=self.post, user=self.user_2, reaction_type="SAD")

    @pytest.mark.django_db
    @freeze_time("2019-08-18")
    def test_get_reactions_to_post(self, setup_data):

        post_storage_object = PostStorageImpl()
        post_reactions_dto = post_storage_object.get_post_reactions(self.post.id, 0, 2)

        reaction_one_data = None
        for reaction in post_reactions_dto:
            if reaction.user_id == self.user_1.id:
                reaction_one_data = reaction

        assert reaction_one_data.name == self.user_1.username
        assert reaction_one_data.profile_pic_url == self.user_1.profile_pic_url
        assert reaction_one_data.reaction_type == self.post_reaction_1.reaction_type
