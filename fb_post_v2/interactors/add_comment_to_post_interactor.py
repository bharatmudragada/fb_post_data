from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class AddCommentToPostInteractor:

    def __init__(self, post_storage: PostStorage, presenter: JsonPresenter):
        self.post_storage = post_storage
        self.presenter = presenter

    def add_comment_to_post(self, post_id: int, comment_user_id: int, comment_text: str):
        comment_dto = self.post_storage.add_comment_to_post(post_id, comment_user_id, comment_text)
        response = self.presenter.add_comment_to_post(comment_dto)
        return response
