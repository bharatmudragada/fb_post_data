from freezegun import freeze_time

from fb_post_v2.interactors.storages.post_storage import CommentReactionDTO
from fb_post_v2.presenters.json_presenter import JsonPresenterImpl


class TestReactToCommentResponse:

    @freeze_time("2019-08-18")
    def test_react_to_comment_response(self):

        comment_reaction_dto = CommentReactionDTO(reaction_id=1, user_id=1, reaction_type="LOVE", comment_id=1)

        json_presenter = JsonPresenterImpl()
        response = json_presenter.get_react_to_comment_response(comment_reaction_dto)

        assert response["reaction_id"] == comment_reaction_dto.reaction_id

    @freeze_time("2019-08-18")
    def test_react_to_comment_response_delete_case(self):

        comment_reaction_dto = None

        json_presenter = JsonPresenterImpl()
        response = json_presenter.get_react_to_comment_response(comment_reaction_dto)

        assert response["status"] == "Reaction Deleted"
