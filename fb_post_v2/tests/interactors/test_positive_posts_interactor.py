import unittest
from unittest.mock import create_autospec

from fb_post_v2.interactors.get_positive_posts_interactor import GetPositivePostsInteractor
from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage, PostIdsDTO


class TestGetPositivePostsInteractor(unittest.TestCase):

    def test_positive_posts(self):
        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        post_ids = [1, 2, 3]
        response_data = {"post_ids": post_ids}

        post_ids_dto = PostIdsDTO(post_ids=post_ids)
        post_storage_mock.get_positive_posts.return_value = post_ids_dto
        presenter_mock.get_positive_posts_response.return_value = response_data

        get_positive_posts_interactor = GetPositivePostsInteractor(post_storage_mock, presenter_mock)
        response = get_positive_posts_interactor.get_positive_posts()

        post_storage_mock.get_positive_posts.assert_called_once_with()
        presenter_mock.get_positive_posts_response.assert_called_once_with(post_ids_dto)
        assert response == response_data
