import unittest
from unittest.mock import create_autospec

from fb_post_v2.interactors.get_posts_reacted_by_user_interactor import GetPostsReactedByUserInteractor
from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage, ReactionDetailsDTO


class TestGetPostsReactedByUser(unittest.TestCase):

    def test_get_post_reacted_by_user(self):
        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        user_id = 1
        response_data = {"reaction_data": "reactions"}

        reactions_dto = [ReactionDetailsDTO(user_id=1, name="user", profile_pic_url="url", reaction_type="LOVE")]
        post_storage_mock.get_posts_reacted_by_user.return_value = reactions_dto
        presenter_mock.get_posts_reacted_by_user_response.return_value = response_data

        get_reactions_to_post_interactor = GetPostsReactedByUserInteractor(post_storage_mock, presenter_mock)
        response = get_reactions_to_post_interactor.get_posts_reacted_by_user(user_id)

        post_storage_mock.get_posts_reacted_by_user.assert_called_once_with(user_id)
        presenter_mock.get_posts_reacted_by_user_response.assert_called_once_with(reactions_dto)
        assert response == response_data
