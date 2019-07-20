import unittest
from unittest.mock import create_autospec

from fb_post_v2.interactors.get_post_interactor import GetPostInteractor
from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage, GetPostDTO


class TestGetPostInteractor(unittest.TestCase):

    def test_get_post(self):
        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        post_id = 1
        response_data = {"post_id": post_id}

        get_post_dto = create_autospec(GetPostDTO)
        post_storage_mock.get_post.return_value = get_post_dto
        presenter_mock.get_post_response.return_value = response_data

        get_post_interactor = GetPostInteractor(post_storage_mock, presenter_mock)
        response = get_post_interactor.get_post(post_id)

        post_storage_mock.get_post.assert_called_once_with(post_id)
        presenter_mock.get_post_response.assert_called_once_with(get_post_dto)
        assert response == response_data
