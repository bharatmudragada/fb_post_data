import unittest
from unittest.mock import create_autospec

from django_swagger_utils.drf_server.exceptions import BadRequest

from fb_post_v2.interactors.delete_post_interactor import DeletePostInteractor
from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class TestDeletePost(unittest.TestCase):

    def test_post_exists(self):

        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        post_id = 1
        response_data = {"status": "post deleted"}

        post_storage_mock.post_exists.return_value = True
        post_storage_mock.delete_post.return_value = response_data
        presenter_mock.get_delete_post_response.return_value = response_data

        delete_post_interactor = DeletePostInteractor(post_storage_mock, presenter_mock)
        response = delete_post_interactor.delete_post(post_id)

        post_storage_mock.post_exists.assert_called_once_with(post_id)
        post_storage_mock.delete_post.assert_called_once_with(post_id)
        presenter_mock.get_delete_post_response.assert_called_once_with(response_data)
        assert response == response_data

    def test_post_does_not_exists(self):

        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        post_id = 1

        post_storage_mock.post_exists.return_value = False
        presenter_mock.raise_post_does_not_exist_exception.side_effect = BadRequest

        delete_post_interactor = DeletePostInteractor(post_storage_mock, presenter_mock)
        with self.assertRaises(BadRequest):
            delete_post_interactor.delete_post(post_id)

        post_storage_mock.post_exists.assert_called_once_with(post_id)
