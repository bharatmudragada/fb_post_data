from freezegun import freeze_time

from fb_post_v2.interactors.storages.post_storage import PostReactionDTO
from fb_post_v2.presenters.json_presenter import JsonPresenterImpl


class TestReactToPostResponse:

    @freeze_time("2019-08-18")
    def test_react_to_post_response(self):

        post_reaction_dto = PostReactionDTO(
            reaction_id=1, user_id=1, reaction_type="LOVE", post_id=1)

        json_presenter = JsonPresenterImpl()
        response = json_presenter.get_react_to_post_response(post_reaction_dto)

        assert response["reaction_id"] == post_reaction_dto.reaction_id

    @freeze_time("2019-08-18")
    def test_react_to_post_response_delete_case(self):

        post_reaction_dto = None

        json_presenter = JsonPresenterImpl()
        response = json_presenter.get_react_to_post_response(post_reaction_dto)

        assert response["status"] == "Reaction Deleted"
