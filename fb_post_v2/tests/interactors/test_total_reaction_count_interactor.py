import unittest
from unittest.mock import create_autospec

from fb_post_v2.interactors.get_total_reaction_count_interactor import GetTotalReactionCountInteractor
from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class TestGetTotalReactionCount(unittest.TestCase):

    def test_get_total_reaction_count(self):
        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        total_reactions_count = 3
        response_data = {"count": total_reactions_count}

        post_storage_mock.get_total_reaction_count.return_value = total_reactions_count
        presenter_mock.get_total_reaction_count_response.return_value = response_data

        get_total_reactions_interactor = GetTotalReactionCountInteractor(post_storage_mock, presenter_mock)
        response = get_total_reactions_interactor.get_total_reaction_count()

        post_storage_mock.get_total_reaction_count.assert_called_once_with()
        presenter_mock.get_total_reaction_count_response.assert_called_once_with(total_reactions_count)
        assert response == response_data
