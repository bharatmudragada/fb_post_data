from fb_post_v2.presenters.json_presenter import JsonPresenterImpl


class TestTotalReactionCountResponse:

    def test_total_reactions_count_response(self):

        total_reactions_count = 5

        json_presenter = JsonPresenterImpl()
        response = json_presenter.get_total_reaction_count_response(total_reactions_count)

        assert response["count"] == total_reactions_count
