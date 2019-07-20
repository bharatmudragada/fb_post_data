from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class GetReactionsToPostInteractor:

    def __init__(self, post_storage: PostStorage, presenter: JsonPresenter):
        self.post_storage = post_storage
        self.presenter = presenter

    def get_reactions_to_post(self, post_id: int):
        reactions_dto = self.post_storage.get_reactions_to_post(post_id)
        response = self.presenter.get_reactions_to_post_response(reactions_dto)
        return response
