import unittest
from unittest.mock import create_autospec

from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.reaction_interactor import ReactionInteractor
from fb_post_v2.interactors.storages.post_storage import PostStorage, CommentReactionDTO, PostReactionDTO


class TestReactToComment(unittest.TestCase):
    
    def test_with_new_reaction(self):

        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        comment_reaction_dto = CommentReactionDTO(reaction_id=1, user_id=1, reaction_type="LOVE", comment_id=1)

        post_storage_mock.comment_reaction_exists.return_value = False
        post_storage_mock.add_reaction_to_comment.return_value = comment_reaction_dto
        presenter_mock.get_react_to_comment_response.return_value = {"reaction_id": 1}

        reaction_interactor = ReactionInteractor(post_storage_mock, presenter_mock)
        response = reaction_interactor.react_to_comment(1, 1, "LOVE")

        post_storage_mock.comment_reaction_exists.assert_called_once_with(1, 1)
        post_storage_mock.add_reaction_to_comment.assert_called_once_with(1, 1, "LOVE")
        presenter_mock.get_react_to_comment_response.assert_called_once_with(comment_reaction_dto)
        assert response == {"reaction_id": 1}

    def test_with_different_reaction(self):

        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        comment_reaction_dto = CommentReactionDTO(reaction_id=1, user_id=1, reaction_type="LOVE", comment_id=1)

        post_storage_mock.comment_reaction_exists.return_value = True
        post_storage_mock.get_comment_reaction.return_value = "LIKE"
        post_storage_mock.update_comment_reaction.return_value = comment_reaction_dto
        presenter_mock.get_react_to_comment_response.return_value = {"reaction_id": 1}

        reaction_interactor = ReactionInteractor(post_storage_mock, presenter_mock)
        response = reaction_interactor.react_to_comment(1, 1, "LOVE")

        post_storage_mock.comment_reaction_exists.assert_called_once_with(1, 1)
        post_storage_mock.get_comment_reaction.assert_called_once_with(1, 1)
        post_storage_mock.update_comment_reaction.assert_called_once_with(1, 1, "LOVE")
        presenter_mock.get_react_to_comment_response.assert_called_once_with(comment_reaction_dto)
        assert response == {"reaction_id": 1}

    def test_with_same_reaction(self):

        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        comment_reaction_dto = None

        post_storage_mock.comment_reaction_exists.return_value = True
        post_storage_mock.get_comment_reaction.return_value = "LOVE"
        post_storage_mock.delete_comment_reaction.return_value = comment_reaction_dto
        presenter_mock.get_react_to_comment_response.return_value = {"status": "reaction_deleted"}

        reaction_interactor = ReactionInteractor(post_storage_mock, presenter_mock)
        response = reaction_interactor.react_to_comment(1, 1, "LOVE")

        post_storage_mock.comment_reaction_exists.assert_called_once_with(1, 1)
        post_storage_mock.get_comment_reaction.assert_called_once_with(1, 1)
        post_storage_mock.delete_comment_reaction.assert_called_once_with(1, 1)
        presenter_mock.get_react_to_comment_response.assert_called_once_with(comment_reaction_dto)
        assert response == {"status": "reaction_deleted"}


class TestReactToPost(unittest.TestCase):
    
    def test_with_new_reaction(self):

        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        post_reaction_dto = PostReactionDTO(reaction_id=1, user_id=1, reaction_type="LOVE", post_id=1)

        post_storage_mock.post_reaction_exists.return_value = False
        post_storage_mock.add_reaction_to_post.return_value = post_reaction_dto
        presenter_mock.get_react_to_post_response.return_value = {"reaction_id": 1}

        reaction_interactor = ReactionInteractor(post_storage_mock, presenter_mock)
        response = reaction_interactor.react_to_post(1, 1, "LOVE")

        post_storage_mock.post_reaction_exists.assert_called_once_with(1, 1)
        post_storage_mock.add_reaction_to_post.assert_called_once_with(1, 1, "LOVE")
        presenter_mock.get_react_to_post_response.assert_called_once_with(post_reaction_dto)
        assert response == {"reaction_id": 1}

    def test_with_different_reaction(self):

        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        post_reaction_dto = PostReactionDTO(reaction_id=1, user_id=1, reaction_type="LOVE", post_id=1)

        post_storage_mock.post_reaction_exists.return_value = True
        post_storage_mock.get_post_reaction.return_value = "LIKE"
        post_storage_mock.update_post_reaction.return_value = post_reaction_dto
        presenter_mock.get_react_to_post_response.return_value = {"reaction_id": 1}

        reaction_interactor = ReactionInteractor(post_storage_mock, presenter_mock)
        response = reaction_interactor.react_to_post(1, 1, "LOVE")

        post_storage_mock.post_reaction_exists.assert_called_once_with(1, 1)
        post_storage_mock.get_post_reaction.assert_called_once_with(1, 1)
        post_storage_mock.update_post_reaction.assert_called_once_with(1, 1, "LOVE")
        presenter_mock.get_react_to_post_response.assert_called_once_with(post_reaction_dto)
        assert response == {"reaction_id": 1}

    def test_with_same_reaction(self):

        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        post_reaction_dto = None

        post_storage_mock.post_reaction_exists.return_value = True
        post_storage_mock.get_post_reaction.return_value = "LOVE"
        post_storage_mock.delete_post_reaction.return_value = post_reaction_dto
        presenter_mock.get_react_to_post_response.return_value = {"status": "reaction_deleted"}

        reaction_interactor = ReactionInteractor(post_storage_mock, presenter_mock)
        response = reaction_interactor.react_to_post(1, 1, "LOVE")

        post_storage_mock.post_reaction_exists.assert_called_once_with(1, 1)
        post_storage_mock.get_post_reaction.assert_called_once_with(1, 1)
        post_storage_mock.delete_post_reaction.assert_called_once_with(1, 1)
        presenter_mock.get_react_to_post_response.assert_called_once_with(post_reaction_dto)
        assert response == {"status": "reaction_deleted"}
