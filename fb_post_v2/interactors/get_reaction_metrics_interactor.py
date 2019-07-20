from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class GetReactionMetricsInteractor:

    def __init__(self, post_storage: PostStorage, presenter: JsonPresenter):
        self.post_storage = post_storage
        self.presenter = presenter

    def get_reaction_metrics(self, post_id: int):
        reaction_metrics_dto = self.post_storage.get_reaction_metrics(post_id)
        response = self.presenter.get_reaction_metrics_response(reaction_metrics_dto)
        return response
