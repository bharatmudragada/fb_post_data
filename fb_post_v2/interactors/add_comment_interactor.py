from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class AddCommentInteractor:

    def __init__(self, post_storage: PostStorage, presenter: JsonPresenter):
        self.post_storage = post_storage
        self.presenter = presenter

    def add_comment_to_post(self, post_id: int, comment_user_id: int, comment_text: str):
        comment_dto = self.post_storage.add_comment_to_post(post_id, comment_user_id, comment_text)
        response = self.presenter.get_add_comment_to_post_response(comment_dto)
        return response

    def add_reply_to_comment(self, comment_id: int, reply_user_id: int, reply_text: str):
        is_reply = self.post_storage.is_reply(comment_id)
        if is_reply:
            comment_id = self.post_storage.get_comment_id_for_reply(comment_id)
        comment_dto = self.post_storage.add_reply_to_comment(comment_id, reply_user_id, reply_text)
        response = self.presenter.get_add_reply_to_comment_response(comment_dto)
        return response
