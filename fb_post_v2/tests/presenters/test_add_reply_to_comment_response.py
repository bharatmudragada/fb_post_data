from freezegun import freeze_time

from fb_post_v2.interactors.storages.post_storage import CommentDTO
from datetime import datetime

from fb_post_v2.presenters.json_presenter import JsonPresenterImpl


class TestAddReplyToCommentResponse:

    @freeze_time("2019-08-18")
    def test_add_reply_to_comment(self):

        comment_dto = CommentDTO(comment_id=2, user_id=1, commented_at=datetime.now(), comment_content="This is a reply", commented_on_id=1)

        json_presenter = JsonPresenterImpl()
        response = json_presenter.get_add_reply_to_comment_response(comment_dto)

        assert response["reply_id"] == comment_dto.comment_id
