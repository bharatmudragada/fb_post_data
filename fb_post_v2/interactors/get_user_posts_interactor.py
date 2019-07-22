from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class GetUserPostsInteractor:

    def __init__(self, post_storage: PostStorage, presenter: JsonPresenter):
        self.post_storage = post_storage
        self.presenter = presenter

    def get_user_posts(self, user_id: int, offset: int, length: int):
        user_posts_dto = self.post_storage.get_user_posts(user_id, offset, length)
        response = self.presenter.get_user_posts_response(user_posts_dto)
        return response
