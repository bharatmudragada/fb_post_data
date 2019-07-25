from freezegun import freeze_time

from fb_post_v2.interactors.storages.post_storage import CommentDTO
from datetime import datetime

from fb_post_v2.presenters.json_presenter import JsonPresenterImpl


class TestAddCommentToPostResponse:

    @freeze_time("2019-08-18")
    def test_add_comment_to_post(self):

        comment_dto = CommentDTO(
            comment_id=1, user_id=1, commented_at=datetime.now(),
            comment_content="This is a comment", commented_on_id=None)

        json_presenter = JsonPresenterImpl()
        response = json_presenter.get_add_comment_to_post_response(comment_dto)

        assert response["comment_id"] == comment_dto.comment_id
