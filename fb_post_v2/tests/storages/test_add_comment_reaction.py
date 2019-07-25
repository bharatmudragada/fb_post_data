import pytest
from freezegun import freeze_time

from fb_post_v2.storages.post_storage import PostStorageImpl
from fb_post_v2.models.models import *


class TestAddCommentReaction:

    @pytest.fixture
    def setup_data(self):
        self.user_1 = User.objects.create(
            username="user_1", profile_pic_url="https://user_1")
        self.post = Post.objects.create(
            user=self.user_1, post_content="This is new post")
        self.comment = Comment.objects.create(
            post=self.post, user=self.user_1, commented_on=None,
            comment_text="This is comment")

    @pytest.mark.django_db
    @freeze_time("2019-08-18")
    def test_add_reaction_to_comment_response(self, setup_data):

        post_storage_object = PostStorageImpl()
        comment_reaction_dto = post_storage_object.add_comment_reaction(
            user_id=self.user_1.id, comment_id=self.comment.id,
            reaction_type="LIKE")

        print(comment_reaction_dto)

        comment_reaction = CommentReactions.objects.filter(
            comment_id=self.comment.id).first()

        print(comment_reaction)

        assert comment_reaction_dto.reaction_id == comment_reaction.id
        assert comment_reaction_dto.user_id == comment_reaction.user_id
        assert comment_reaction_dto.reaction_type == comment_reaction\
            .reaction_type
        assert comment_reaction_dto.comment_id == comment_reaction.comment_id
