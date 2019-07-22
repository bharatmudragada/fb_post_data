import unittest

from mock import create_autospec, Mock
from fb_post_v2.models.models import Comment
from fb_post_v2.storages.post_storage import PostStorage
from unittest.mock import patch


class TestIsReply(unittest.TestCase):

    @patch('fb_post_v2.storages.post_storage.Comment')
    def test_is_reply_with_comment(self, comment_mock):

        comment = create_autospec(Comment)
        comment.commented_on = None
        comment_mock.objects.get.return_value = comment

        post_storage_object = PostStorage()
        response = post_storage_object.is_reply(3)

        comment_mock.objects.get.assert_called_once_with(pk=3)
        assert response == False

    @patch('fb_post_v2.storages.post_storage.Comment')
    def test_is_reply_with_reply(self, comment_mock):

        comment = Mock()
        comment.commented_on = 2
        comment_mock.objects.get.return_value = comment

        post_storage_object = PostStorage()
        response = post_storage_object.is_reply(3)

        comment_mock.objects.get.assert_called_once_with(pk=3)
        assert response == True
