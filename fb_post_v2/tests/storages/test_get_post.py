import pytest
import unittest

from unittest.mock import create_autospec
from unittest.mock import patch

from freezegun import freeze_time

from fb_post_v2.models.models import *
from fb_post_v2.storages.post_storage import PostStorage


class TestGetPost:

    def setup_user_data(self):
        self.user_1 = User.objects.create(username="user_5", profile_pic_url="https://user_1")
        self.user_2 = User.objects.create(username="user_6", profile_pic_url="https://user_2")
        self.user_3 = User.objects.create(username="user_7", profile_pic_url="https://user_3")
        self.user_4 = User.objects.create(username="user_8", profile_pic_url="https://user_4")

    def setup_comment_data(self):
        self.comment = Comment.objects.create(post=self.post, commented_on=None, user=self.user_1, comment_text="This is comment")
        self.reply = Comment.objects.create(post=self.post, commented_on=self.comment, user=self.user_2, comment_text="This is reply")
        self.comment_reaction = CommentReactions.objects.create(comment=self.comment, user=self.user_2, reaction_type="LOVE")
        self.comment_reaction_2 = CommentReactions.objects.create(comment=self.comment, user=self.user_3, reaction_type="LOVE")
        self.comment_reaction_3 = CommentReactions.objects.create(comment=self.comment, user=self.user_4, reaction_type="WOW")

    @freeze_time("2019-08-18")
    @pytest.fixture
    def setup_data(self):
        self.setup_user_data()
        self.post = Post.objects.create(user=self.user_1, post_content="This is first post")
        self.post_reaction_1 = PostReactions.objects.create(post=self.post, user=self.user_2, reaction_type="WOW")
        self.post_reaction_2 = PostReactions.objects.create(post=self.post, user=self.user_3, reaction_type="WOW")
        self.setup_comment_data()

        return self.post

    @pytest.mark.django_db
    def test_get_post(self, setup_data):

        post_storage_object = PostStorage()
        get_post_dto = post_storage_object.get_post(post_id=1)
        print(get_post_dto)

        post_details = get_post_dto.post_details
        assert post_details.post_id == self.post.id
        assert post_details.user_id == self.post.user_id
        assert post_details.post_content == self.post.post_content
        assert post_details.created_time == self.post.posted_time

        posted_by_user = get_post_dto.posted_by
        assert posted_by_user.user_id == self.user_1.id
        assert posted_by_user.name == self.user_1.username
        assert posted_by_user.profile_pic_url == self.user_1.profile_pic_url

        post_reactions = get_post_dto.post_reaction_data
        assert post_reactions.count == 2
        assert ["WOW"].sort() == post_reactions.type.sort()

        comments = get_post_dto.comments

        assert self.comment.id in [comment.comment_id for comment in comments]

        comment_data = None
        for comment in comments:
            if comment.comment_id == self.comment.id:
                comment_data = comment

        comment_user = comment_data.user
        assert comment_user.user_id == self.user_1.id
        assert comment_user.name == self.user_1.username
        assert comment_user.profile_pic_url == self.user_1.profile_pic_url

        assert comment_data.commented_at == self.comment.commented_time
        assert comment_data.comment_content == self.comment.comment_text

        comment_reactions = comment_data.comment_reactions
        assert comment_reactions.count == 3
        assert comment_reactions.type.sort() == ["LOVE", "WOW"].sort()

        assert self.reply.id in [reply.comment_id for reply in comment_data.replies]

        reply_data = None
        for reply in comment_data.replies:
            if reply.comment_id == self.reply.id:
                reply_data = reply

        reply_user = reply_data.user
        assert reply_user.user_id == self.user_2.id
        assert reply_user.name == self.user_2.username
        assert reply_user.profile_pic_url == self.user_2.profile_pic_url

        assert reply_data.commented_at == self.reply.commented_time
        assert reply_data.comment_content == self.reply.comment_text

        reply_reactions = reply_data.comment_reactions
        assert reply_reactions.count == 0
        assert reply_reactions.type == []