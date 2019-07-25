import pytest
from freezegun import freeze_time

from fb_post_v2.storages.post_storage import PostStorageImpl
from fb_post_v2.models.models import *


class TestAddPostReaction:

    @pytest.fixture
    def setup_data(self):
        self.user_1 = User.objects.create(username="user_1", profile_pic_url="https://user_1")
        self.post = Post.objects.create(user=self.user_1, post_content="This is new post")

    @pytest.mark.django_db
    @freeze_time("2019-08-18")
    def test_add_reaction_to_post_response(self, setup_data):

        post_storage_object = PostStorageImpl()
        post_reaction_dto = post_storage_object.add_post_reaction(user_id=self.user_1.id, post_id=self.post.id, reaction_type="LOVE")

        post_reaction = PostReactions.objects.filter(post_id=self.post.id).first()

        assert post_reaction_dto.reaction_id == post_reaction.id
        assert post_reaction_dto.user_id == post_reaction.user_id
        assert post_reaction_dto.reaction_type == post_reaction.reaction_type
        assert post_reaction_dto.post_id == post_reaction.post_id

