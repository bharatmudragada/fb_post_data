import unittest
from unittest.mock import create_autospec

from fb_post_v2.interactors.get_positive_posts_interactor import GetPostsWithMorePositiveReactionsInteractor
from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class TestGetPositivePostsInteractor(unittest.TestCase):

    def test_positive_posts(self):
        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        post_ids = [1, 2, 3]
        response_data = {"post_ids": post_ids}

        post_storage_mock.get_posts_with_more_positive_reactions.return_value = post_ids
        presenter_mock.get_posts_with_more_positive_reactions_response.return_value = response_data

        get_positive_posts_interactor = GetPostsWithMorePositiveReactionsInteractor(post_storage_mock, presenter_mock)
        response = get_positive_posts_interactor.get_positive_posts()

        post_storage_mock.get_posts_with_more_positive_reactions.assert_called_once_with()
        presenter_mock.get_posts_with_more_positive_reactions_response.assert_called_once_with(post_ids)
        assert response == response_data
