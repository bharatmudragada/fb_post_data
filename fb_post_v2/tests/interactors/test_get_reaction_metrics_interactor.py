import unittest
from unittest.mock import create_autospec

from fb_post_v2.interactors.get_reaction_metrics_interactor import GetReactionMetricsInteractor
from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage, ReactionMetricDTO


class TestGetReactionMetrics(unittest.TestCase):

    def test_get_reaction_metrics(self):
        post_storage_mock = create_autospec(PostStorage)
        presenter_mock = create_autospec(JsonPresenter)

        post_id = 1
        response_data = [{"reaction_type": "LOVE", "count": 3}]

        reaction_metrics_dto = [ReactionMetricDTO(reaction_type="LOVE", count=3)]
        post_storage_mock.get_reaction_metrics.return_value = reaction_metrics_dto
        presenter_mock.get_reaction_metrics_response.return_value = response_data

        get_reaction_metric_interactor = GetReactionMetricsInteractor(post_storage_mock, presenter_mock)
        response = get_reaction_metric_interactor.get_reaction_metrics(post_id)

        post_storage_mock.get_reaction_metrics.assert_called_once_with(post_id)
        presenter_mock.get_reaction_metrics_response.assert_called_once_with(reaction_metrics_dto)
        assert response == response_data
