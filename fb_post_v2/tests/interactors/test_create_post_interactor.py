import unittest

from datetime import datetime
from mock import create_autospec

from fb_post_v2.interactors.create_post_interactor import CreatePostInteractor
from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage, PostDTO


class TestCreatePost(unittest.TestCase):

    def test_create_post(self):
        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        post_id = 1
        user_id = 1
        post_content = "This is a post"
        response_data = {"post_id": post_id}

        post_dto = PostDTO(
            post_id=post_id, user_id=user_id, post_content=post_content,
            created_time=datetime.now())

        post_storage_mock.create_post.return_value = post_dto
        presenter_mock.get_create_post_response.return_value = response_data

        create_post_interactor = CreatePostInteractor(post_storage_mock,
                                                      presenter_mock)
        response = create_post_interactor.create_post(post_content, user_id)

        post_storage_mock.create_post.assert_called_once_with(post_content,
                                                              user_id)
        presenter_mock.get_create_post_response.assert_called_once_with(post_dto)
        assert response == response_data
