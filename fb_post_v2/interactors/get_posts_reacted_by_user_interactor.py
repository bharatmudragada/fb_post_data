from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class GetPostsReactedByUserInteractor:

    def __init__(self, post_storage: PostStorage, presenter: JsonPresenter):
        self.post_storage = post_storage
        self.presenter = presenter

    def get_posts_reacted_by_user(self, user_id: int):
        post_ids_dto = self.post_storage.get_posts_reacted_by_user(user_id)
        response = self.presenter.get_posts_reacted_by_user_response(post_ids_dto)
        return response
