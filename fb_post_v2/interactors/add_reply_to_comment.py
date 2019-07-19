from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class AddReplyToCommentInteractor:

    def __init__(self, post_storage: PostStorage, presenter: JsonPresenter):
        self.post_storage = post_storage
        self.presenter = presenter

    def add_reply_to_comment(self, comment_id: int, reply_user_id: int, reply_text: str):
        comment_dto = self.post_storage.add_comment_to_post(comment_id, reply_user_id, reply_text)
        response = self.presenter.add_comment_to_post(comment_dto)
        return response
