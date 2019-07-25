import unittest
from unittest.mock import create_autospec
from datetime import datetime

from fb_post_v2.interactors.add_comment_interactor import AddCommentInteractor
from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage, CommentDTO


class TestAddCommentToPost(unittest.TestCase):
    
    def test_add_comment_to_post(self):
        
        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        post_id = 1
        comment_id = 1
        user_id = 1
        commented_on_id = None
        comment_text = "This is comment"
        response_data = {"comment_id": comment_id}

        comment_dto = CommentDTO(
            comment_id=comment_id, user_id=user_id, commented_at=datetime.now(),
            commented_on_id=commented_on_id, comment_content=comment_text)
        
        post_storage_mock.add_comment_to_post.return_value = comment_dto
        presenter_mock.get_add_comment_to_post_response.return_value =\
            response_data

        add_comment_interactor = AddCommentInteractor(
            post_storage_mock, presenter_mock)
        response = add_comment_interactor.add_comment_to_post(
            post_id, user_id, comment_text)

        post_storage_mock.add_comment_to_post.assert_called_once_with(
            post_id, user_id, comment_text)
        presenter_mock.get_add_comment_to_post_response.assert_called_once_with(
            comment_dto)
        assert response == response_data


class TestAddReplyToComment(unittest.TestCase):

    def test_reply_to_reply(self):

        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        comment_id = 2
        reply_user_id = 1
        reply_text = "This is reply"
        reply_id = 4
        commented_on_id = 1
        response_data = {"reply_id": reply_id}

        comment_dto = CommentDTO(
            comment_id=reply_id, user_id=reply_user_id,
            commented_at=datetime.now(), commented_on_id=commented_on_id,
            comment_content=reply_text)

        post_storage_mock.is_reply.return_value = True
        post_storage_mock.get_comment_id_for_reply.return_value = \
            commented_on_id
        post_storage_mock.add_reply_to_comment.return_value = comment_dto
        presenter_mock.get_add_reply_to_comment_response.return_value =\
            response_data

        add_comment_interactor = AddCommentInteractor(
            post_storage_mock, presenter_mock)
        response = add_comment_interactor.add_reply_to_comment(
            comment_id, reply_user_id, reply_text)

        post_storage_mock.is_reply.assert_called_once_with(comment_id)
        post_storage_mock.get_comment_id_for_reply.assert_called_once_with(
            comment_id)
        post_storage_mock.add_reply_to_comment.assert_called_once_with(
            commented_on_id, reply_user_id, reply_text)
        presenter_mock.get_add_reply_to_comment_response\
            .assert_called_once_with(comment_dto)
        assert response == response_data

    def test_reply_to_comment(self):

        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        comment_id = 1
        reply_user_id = 1
        reply_text = "This is reply"
        reply_id = 4
        response_data = {"reply_id": reply_id}

        comment_dto = CommentDTO(
            comment_id=reply_id, user_id=reply_user_id,
            commented_at=datetime.now(), commented_on_id=comment_id,
            comment_content=reply_text)

        post_storage_mock.is_reply.return_value = False
        post_storage_mock.add_reply_to_comment.return_value = comment_dto
        presenter_mock.get_add_reply_to_comment_response.return_value = \
            response_data

        add_comment_interactor = AddCommentInteractor(post_storage_mock,
                                                      presenter_mock)
        response = add_comment_interactor.add_reply_to_comment(
            comment_id, reply_user_id, reply_text)

        post_storage_mock.is_reply.assert_called_once_with(comment_id)
        post_storage_mock.add_reply_to_comment(comment_id, reply_user_id,
                                               reply_text)
        presenter_mock.get_add_reply_to_comment_response\
            .assert_called_once_with(comment_dto)
        assert response == response_data
