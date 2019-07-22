import unittest

from mock import create_autospec

from fb_post_v2.models.models import Post
from fb_post_v2.storages.post_storage import PostStorage
from unittest.mock import patch
from django.core.exceptions import ObjectDoesNotExist


class TestPostExists(unittest.TestCase):

    @patch('fb_post_v2.storages.post_storage.Post')
    def test_post_exists_returns_false(self, post_mock):

        post_mock.objects.get.side_effect = ObjectDoesNotExist

        post_storage_object = PostStorage()
        response = post_storage_object.post_exists(post_id=1)

        post_mock.objects.get.assert_called_once_with(pk=1)
        assert response == False

    @patch('fb_post_v2.storages.post_storage.Post')
    def test_post_exists_returns_true(self, post_mock):

        post = create_autospec(Post)
        post_mock.objects.get.return_value = post

        post_storage_object = PostStorage()
        response = post_storage_object.post_exists(post_id=1)

        post_mock.objects.get.assert_called_once_with(pk=1)
        assert response == True
