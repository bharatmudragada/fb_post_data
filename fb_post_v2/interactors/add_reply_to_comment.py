from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class AddReplyToCommentInteractor:

    def __init__(self, post_storage: PostStorage, presenter: JsonPresenter):
        self.post_storage = post_storage
        self.presenter = presenter

    def add_reply_to_comment(self, comment_id: int, reply_user_id: int, reply_text: str):
        is_comment = self.post_storage.is_comment(comment_id)
        if not is_comment:
            comment_id = self.post_storage.get_comment_id(comment_id)
        comment_dto = self.post_storage.add_reply_to_comment(comment_id, reply_user_id, reply_text)
        response = self.presenter.add_reply_to_comment(comment_dto)
        return response
