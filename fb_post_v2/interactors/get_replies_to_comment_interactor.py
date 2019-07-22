from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class GetRepliesToCommentInteractor:

    def __init__(self, post_storage: PostStorage, presenter: JsonPresenter):
        self.post_storage = post_storage
        self.presenter = presenter

    def get_replies_to_comment(self, comment_id: int, offset: int, length: int):
        is_reply = self.post_storage.is_reply(comment_id)
        if is_reply:
            return self.presenter.raise_not_a_comment_exception()
        else:
            replies_dto = self.post_storage.get_replies_to_comment(comment_id, offset, length)
            response = self.presenter.get_replies_to_comment_response(replies_dto)
            return response
