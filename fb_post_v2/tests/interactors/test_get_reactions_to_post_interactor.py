import unittest
from unittest.mock import create_autospec

from fb_post_v2.interactors.get_reactions_to_post_interactor import GetReactionsToPostInteractor
from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage, ReactionDetailsDTO


class TestGetReactionsToPost(unittest.TestCase):

    def test_get_reactions_to_post(self):
        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        post_id = 1
        response_data = [{"user_id": 1, "name": "user", "profile_pic_url": "url", "reaction_type": "LOVE"}]

        reactions_dto = [ReactionDetailsDTO(user_id=1, name="user", profile_pic_url="url", reaction_type="LOVE")]
        post_storage_mock.get_reactions_to_post.return_value = reactions_dto
        presenter_mock.get_reactions_to_post_response.return_value = response_data

        get_reactions_to_post_interactor = GetReactionsToPostInteractor(post_storage_mock, presenter_mock)
        response = get_reactions_to_post_interactor.get_reactions_to_post(post_id)

        post_storage_mock.get_reactions_to_post.assert_called_once_with(post_id)
        presenter_mock.get_reactions_to_post_response.assert_called_once_with(reactions_dto)
        assert response == response_data
