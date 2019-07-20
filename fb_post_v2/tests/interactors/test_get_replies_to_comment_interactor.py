import unittest
from unittest.mock import create_autospec

from django_swagger_utils.drf_server.exceptions import BadRequest

from fb_post_v2.interactors.get_replies_to_comment_interactor import GetRepliesToCommentInteractor
from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage, RepliesDTO


class TestGetRepliesToComment(unittest.TestCase):

    def test_get_replies_to_comment_with_comment(self):
        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        comment_id = 1
        response_data = [{"replies": "reply_data"}]

        replies_dto = create_autospec(RepliesDTO)
        post_storage_mock.is_reply.return_value = False
        post_storage_mock.get_replies_to_comment.return_value = replies_dto
        presenter_mock.get_replies_to_comment_response.return_value = response_data

        get_replies_to_comment_interactor = GetRepliesToCommentInteractor(post_storage_mock, presenter_mock)
        response = get_replies_to_comment_interactor.get_replies_to_comment(comment_id)

        post_storage_mock.is_reply.assert_called_once_with(comment_id)
        post_storage_mock.get_replies_to_comment.assert_called_once_with(comment_id)
        presenter_mock.get_replies_to_comment_response.assert_called_once_with(replies_dto)
        assert response == response_data

    def test_get_replies_to_comment_with_reply(self):
        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        comment_id = 1

        post_storage_mock.is_reply.return_value = True
        presenter_mock.raise_not_a_comment_exception.side_effect = BadRequest

        get_replies_to_comment_interactor = GetRepliesToCommentInteractor(post_storage_mock, presenter_mock)
        with self.assertRaises(BadRequest):
            get_replies_to_comment_interactor.get_replies_to_comment(comment_id)

        post_storage_mock.is_reply.assert_called_once_with(comment_id)
