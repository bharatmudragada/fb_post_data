from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class GetUserPostsInteractor:

    def __init__(self, post_storage: PostStorage, presenter: JsonPresenter):
        self.post_storage = post_storage
        self.presenter = presenter

    def get_positive_posts(self):
        post_ids_dto = self.post_storage.get_positive_posts()
        response = self.presenter.get_positive_posts(post_ids_dto)
        return response
