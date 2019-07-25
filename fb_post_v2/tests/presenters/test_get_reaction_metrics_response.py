from fb_post_v2.interactors.storages.post_storage import ReactionMetricDTO

from fb_post_v2.presenters.json_presenter import JsonPresenterImpl


class TestGetReactionsMetricResponse:

    def test_get_reaction_metrics_response(self):

        love_reaction_metric_dto = ReactionMetricDTO(reaction_type="LOVE", count=2)
        haha_reaction_metric_dto = ReactionMetricDTO(reaction_type="HAHA", count=3)
        reaction_metrics_dto = [love_reaction_metric_dto, haha_reaction_metric_dto]

        json_presenter = JsonPresenterImpl()
        response = json_presenter.get_reaction_metrics_response(reaction_metrics_dto)

        love_reaction_metric = None
        for reaction_metric in response:
            if reaction_metric['reaction_type'] == "LOVE":
                love_reaction_metric = reaction_metric

        assert love_reaction_metric['count'] == love_reaction_metric_dto.count

        haha_reaction_metric = None
        for reaction_metric in response:
            if reaction_metric['reaction_type'] == "HAHA":
                haha_reaction_metric = reaction_metric

        assert haha_reaction_metric['count'] == haha_reaction_metric_dto.count
