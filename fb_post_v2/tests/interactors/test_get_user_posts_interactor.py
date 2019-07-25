import unittest
from unittest.mock import create_autospec

from fb_post_v2.interactors.get_user_posts_interactor import \
    GetUserPostsInteractor
from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage, GetPostDTO


class TestGetUserPosts(unittest.TestCase):

    def test_get_user_posts(self):
        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        user_id = 1
        response_data = {"posts": "post_details"}

        user_posts_dto = create_autospec(GetPostDTO)
        post_storage_mock.get_user_posts.return_value = user_posts_dto
        presenter_mock.get_user_posts_response.return_value = response_data

        get_user_posts_interactor = GetUserPostsInteractor(
            post_storage_mock, presenter_mock)
        response = get_user_posts_interactor.get_user_posts(user_id, 0, 2)

        post_storage_mock.get_user_posts.assert_called_once_with(user_id, 0, 2)
        presenter_mock.get_user_posts_response.assert_called_once_with(
            user_posts_dto)
        assert response == response_data
