from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class GetPostReactionsInteractor:

    def __init__(self, post_storage: PostStorage, presenter: JsonPresenter):
        self.post_storage = post_storage
        self.presenter = presenter

    def get_post_reactions(self, post_id: int, offset: int, length: int):

        reactions_dto = self.post_storage\
            .get_post_reactions(post_id, offset, length)

        response = self.presenter.get_post_reactions_response(reactions_dto)
        return response
