import unittest

from mock import create_autospec

from fb_post_v2.models.models import CommentReactions
from fb_post_v2.storages.post_storage import PostStorageImpl
from unittest.mock import patch
from django.core.exceptions import ObjectDoesNotExist


class TestCommentReactionExists(unittest.TestCase):

    @patch('fb_post_v2.storages.post_storage.CommentReactions')
    def test_comment_reaction_exists_returns_false(self, comment_reaction_mock):

        comment_reaction_mock.objects.get.side_effect = ObjectDoesNotExist

        post_storage_object = PostStorageImpl()
        response = post_storage_object.comment_reaction_exists\
            (user_id=1, comment_id=1)

        comment_reaction_mock.objects.get.assert_called_once_with(
            user_id=1, comment_id=1)
        assert response == False

    @patch('fb_post_v2.storages.post_storage.CommentReactions')
    def test_comment_reaction_exists_returns_true(self, comment_reaction_mock):

        comment_reaction = create_autospec(CommentReactions)
        comment_reaction_mock.objects.get.return_value = comment_reaction

        post_storage_object = PostStorageImpl()
        response = post_storage_object.comment_reaction_exists(
            user_id=1, comment_id=1)

        comment_reaction_mock.objects.get.assert_called_once_with(
            user_id=1, comment_id=1)
        assert response == True
