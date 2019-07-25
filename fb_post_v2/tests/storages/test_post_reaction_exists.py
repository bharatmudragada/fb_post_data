import unittest

from mock import create_autospec

from fb_post_v2.models.models import PostReactions
from fb_post_v2.storages.post_storage import PostStorageImpl
from unittest.mock import patch
from django.core.exceptions import ObjectDoesNotExist


class TestPostReactionExists(unittest.TestCase):

    @patch('fb_post_v2.storages.post_storage.PostReactions')
    def test_post_reaction_exists_returns_false(self, post_reaction_mock):

        post_reaction_mock.objects.get.side_effect = ObjectDoesNotExist

        post_storage_object = PostStorageImpl()
        response = post_storage_object.post_reaction_exists(
            user_id=1, post_id=1)

        post_reaction_mock.objects.get.assert_called_once_with(
            user_id=1, post_id=1)
        assert response == False

    @patch('fb_post_v2.storages.post_storage.PostReactions')
    def test_post_reaction_exists_returns_true(self, post_reaction_mock):

        post_reaction = create_autospec(PostReactions)
        post_reaction_mock.objects.get.return_value = post_reaction

        post_storage_object = PostStorageImpl()
        response = post_storage_object.post_reaction_exists(
            user_id=1, post_id=1)

        post_reaction_mock.objects.get.assert_called_once_with(
            user_id=1, post_id=1)
        assert response == True
