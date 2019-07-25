import unittest
from unittest.mock import create_autospec

from fb_post_v2.interactors.get_posts_reacted_by_user_interactor import GetUserReactedPostsInteractor
from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class TestGetPostsReactedByUser(unittest.TestCase):

    def test_get_post_reacted_by_user(self):
        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        user_id = 1
        post_ids = [1, 2, 3]
        response_data = {"post_ids": post_ids}

        post_storage_mock.get_user_reacted_posts.return_value = post_ids
        presenter_mock.get_user_reacted_posts_response.return_value = response_data

        get_reactions_to_post_interactor = GetUserReactedPostsInteractor(post_storage_mock, presenter_mock)
        response = get_reactions_to_post_interactor.get_posts_reacted_by_user(user_id)

        post_storage_mock.get_user_reacted_posts.assert_called_once_with(user_id)
        presenter_mock.get_user_reacted_posts_response.assert_called_once_with(post_ids)
        assert response == response_data
