import pytest
from datetime import datetime
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

    def test_get_user_dto(self):

        comment = {"user": 1, "user__username": "name", "user__profile_pic_url": "http://profile_pic"}
        post_storage_object = PostStorage()
        user_dto = post_storage_object.get_user_dto(comment)

        assert user_dto.user_id == comment['user']
        assert user_dto.name == comment['user__username']
        assert user_dto.profile_pic_url == comment['user__profile_pic_url']

    def test_get_reactions_dto(self):

        comment_reactions = {"count": 1, "type": ["WOW", "LOVE"]}
        post_storage_object = PostStorage()
        reaction_dto = post_storage_object.get_reaction_dto(comment_reactions)

        assert reaction_dto.count == comment_reactions["count"]
        assert reaction_dto.type == comment_reactions["type"]

    @freeze_time("2019-08-18")
    def test_get_comment_dto_with_out_replies(self):
        comment_reactions = {"count": 1, "type": ["WOW", "LOVE"]}
        comment = {"id": 1, "commented_time": datetime.now(), "comment_text": "This is comment data", "user": 1, "user__username": "name", "user__profile_pic_url": "http://profile_pic"}

        post_storage_object = PostStorage()
        comment_dto = post_storage_object.get_comment_dto_with_out_replies(comment, comment_reactions)

        assert comment_dto.comment_id == comment['id']
        assert comment_dto.commented_at == comment['commented_time']
        assert comment_dto.comment_content == comment['comment_text']

        comment_user = comment_dto.user
        assert comment_user.user_id == comment['user']
        assert comment_user.name == comment['user__username']
        assert comment_user.profile_pic_url == comment['user__profile_pic_url']

        reactions = comment_dto.comment_reactions
        assert reactions.count == comment_reactions['count']
        assert reactions.type == comment_reactions['type']

    @freeze_time("2019-08-18")
    def test_get_comment_dto_with_replies(self):
        comment_reactions = {"count": 1, "type": ["WOW", "LOVE"]}
        comment = {"id": 1, "commented_time": datetime.now(), "comment_text": "This is comment data", "user": 1, "user__username": "name", "user__profile_pic_url": "http://profile_pic"}
        replies = []
        replies_count = 0

        post_storage_object = PostStorage()
        comment_dto_with_replies = post_storage_object.get_comment_dto_with_replies(comment, comment_reactions, replies, replies_count)

        assert comment_dto_with_replies.comment_id == comment['id']
        assert comment_dto_with_replies.commented_at == comment['commented_time']
        assert comment_dto_with_replies.comment_content == comment['comment_text']

        comment_user = comment_dto_with_replies.user
        assert comment_user.user_id == comment['user']
        assert comment_user.name == comment['user__username']
        assert comment_user.profile_pic_url == comment['user__profile_pic_url']

        reactions = comment_dto_with_replies.comment_reactions
        assert reactions.count == comment_reactions['count']
        assert reactions.type == comment_reactions['type']

        assert comment_dto_with_replies.replies == replies
        assert comment_dto_with_replies.replies_count == replies_count

    def test_get_comment_replies(self):

        all_comment_replies = [{"comment_id": 4, "commented_on": 1}, {"comment_id": 5, "commented_on": 1}, {"comment_id": 6, "commented_on": 2}]

        post_storage_object = PostStorage()
        comment_replies = post_storage_object.get_comment_replies(all_comment_replies)

        reply_ids_of_comment_one = [replies['comment_id'] for replies in comment_replies[1]]
        assert 4 in reply_ids_of_comment_one
        assert 5 in reply_ids_of_comment_one
        assert 6 not in reply_ids_of_comment_one

        reply_ids_of_comment_two = [replies['comment_id'] for replies in comment_replies[2]]
        assert 6 in reply_ids_of_comment_two
        assert 4 not in reply_ids_of_comment_two
        assert 5 not in reply_ids_of_comment_two

    def test_get_comment_reactions(self):

        all_comment_reactions = [{'comment_id': 1, 'reaction_type': "WOW"}, {'comment_id': 1, 'reaction_type': "WOW"}, {'comment_id': 2, 'reaction_type': "SAD"}, {'comment_id': 2, 'reaction_type': "WOW"}]

        post_storage_object = PostStorage()
        comment_reactions = post_storage_object.get_comment_reactions(all_comment_reactions)

        comment_one_reactions = comment_reactions[1]
        assert comment_one_reactions['count'] == 2
        assert comment_one_reactions['type'] == set(['WOW'])

        comment_two_reactions = comment_reactions[2]
        assert comment_two_reactions['count'] == 2
        assert comment_two_reactions['type'] == set(['WOW', 'SAD'])

    @freeze_time("2019-08-18")
    def test_get_comment_dto_list(self):

        comments_of_post = [
            {'id': 1, 'commented_on': None, 'user': 1, 'user__username': 'user_1', 'user__profile_pic_url': 'https://user1.png', 'comment_text': 'This is comment one', 'commented_time': datetime.now()},
            {'id': 2, 'commented_on': None, 'user': 1, 'user__username': 'user_1', 'user__profile_pic_url': 'https://user1.png', 'comment_text': 'This is comment two', 'commented_time': datetime.now()},
        ]

        comment_replies = {
            1: [{'id': 3, 'commented_on': 1, 'user': 2, 'user__username': 'user_2', 'user__profile_pic_url': 'https://user2.png', 'comment_text': 'This is reply one', 'commented_time': datetime.now()}],
            2: [{'id': 4, 'commented_on': 2, 'user': 1, 'user__username': 'user_1', 'user__profile_pic_url': 'https://user1.png', 'comment_text': 'This is reply two', 'commented_time': datetime.now()}],
        }

        comment_reactions = {1: {'count': 3, 'type': ['WOW', 'SAD']}, 3: {'count': 1, 'type': ['HAHA']}}

        post_storage_object = PostStorage()
        comments_dto = post_storage_object.get_comment_dto_list(comments_of_post, comment_replies, comment_reactions)

        comment_ids = [comment.comment_id for comment in comments_dto]

        assert 1 in comment_ids
        assert 2 in comment_ids
        assert 3 not in comment_ids
        assert 4 not in comment_ids

        comment_one_dto = None
        for comment in comments_dto:
            if comment.comment_id == 1:
                comment_one_dto = comment

        assert comment_one_dto.user.user_id == comments_of_post[0]['user']
        assert comment_one_dto.user.name == comments_of_post[0]['user__username']
        assert comment_one_dto.user.profile_pic_url == comments_of_post[0]['user__profile_pic_url']
        assert comment_one_dto.comment_content == comments_of_post[0]['comment_text']
        assert comment_one_dto.commented_at == comments_of_post[0]['commented_time']
        assert comment_one_dto.comment_reactions.count == comment_reactions[1]['count']
        assert comment_one_dto.comment_reactions.type == comment_reactions[1]['type']

        comment_two_dto = None
        for comment in comments_dto:
            if comment.comment_id == 2:
                comment_two_dto = comment

        assert comment_two_dto.comment_reactions.count == 0
        assert comment_two_dto.comment_reactions.type == []

        reply_ids_of_comment_one = [reply.comment_id for reply in comment_one_dto.replies]
        
        assert 3 in reply_ids_of_comment_one
        assert 4 not in reply_ids_of_comment_one
        
        reply_three_dto = None
        for reply in comment_one_dto.replies:
            if reply.comment_id == 3:
                reply_three_dto = reply

        assert reply_three_dto.user.user_id == comment_replies[1][0]['user']
        assert reply_three_dto.user.name == comment_replies[1][0]['user__username']
        assert reply_three_dto.user.profile_pic_url == comment_replies[1][0]['user__profile_pic_url']
        assert reply_three_dto.comment_content == comment_replies[1][0]['comment_text']
        assert reply_three_dto.commented_at == comment_replies[1][0]['commented_time']
        assert reply_three_dto.comment_reactions.count == comment_reactions[3]['count']
        assert reply_three_dto.comment_reactions.type == comment_reactions[3]['type']

        reply_four_dto = None
        for reply in comment_two_dto.replies:
            if reply.comment_id == 4:
                reply_four_dto = reply

        assert reply_four_dto.comment_reactions.count == 0
        assert reply_four_dto.comment_reactions.type == []
