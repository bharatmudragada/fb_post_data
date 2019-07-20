from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class GetPostInteractor:

    def __init__(self, post_storage: PostStorage, presenter: JsonPresenter):
        self.post_storage = post_storage
        self.presenter = presenter

    def get_post(self, post_id: int):
        get_post_dto = self.post_storage.get_post(post_id)
        response = self.presenter.get_post_response(get_post_dto)
        return response
