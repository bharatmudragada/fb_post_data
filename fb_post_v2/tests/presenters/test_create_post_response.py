import pytest
from freezegun import freeze_time

from fb_post_v2.interactors.storages.post_storage import PostDTO
from datetime import datetime

from fb_post_v2.presenters.json_presenter import JsonPresenter


class TestCreatePostResponse:

    @freeze_time("2019-08-18")
    def test_create_post_response(self):

        post_dto = PostDTO(post_id=1, user_id=1, post_content="This is a post", created_time=datetime.now())

        json_presenter = JsonPresenter()
        response = json_presenter.get_create_post_response(post_dto)

        assert response["post_id"] == post_dto.post_id
