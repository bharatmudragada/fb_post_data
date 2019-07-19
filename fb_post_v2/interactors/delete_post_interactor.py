from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class DeletePostInteractor:

    def __init__(self, post_storage: PostStorage, presenter: JsonPresenter):
        self.post_storage = post_storage
        self.presenter = presenter

    def create_post(self, post_id: int):
        status_dict = self.post_storage.delete_post(post_id)
        response = self.presenter.delete_post(status_dict)
        return response


