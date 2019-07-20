from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class DeletePostInteractor:

    def __init__(self, post_storage: PostStorage, presenter: JsonPresenter):
        self.post_storage = post_storage
        self.presenter = presenter

    def delete_post(self, post_id: int):
        post_exists = self.post_storage.post_exists(post_id)
        if post_exists:
            status_dict = self.post_storage.delete_post(post_id)
            response = self.presenter.get_delete_post_response(status_dict)
            return response
        return self.presenter.raise_post_does_not_exist_exception()
