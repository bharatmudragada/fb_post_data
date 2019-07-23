from fb_post_v2.interactors.storages.post_storage import TotalReactionsDTO

from fb_post_v2.presenters.json_presenter import JsonPresenter


class TestTotalReactionCountResponse:

    def test_total_reactions_count_response(self):

        total_reaction_dto = TotalReactionsDTO(count=5)

        json_presenter = JsonPresenter()
        response = json_presenter.get_total_reaction_count_response(total_reaction_dto)

        assert response["count"] == total_reaction_dto.count
