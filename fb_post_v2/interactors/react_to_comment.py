from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class ReactToCommentInteractor:

    def __init__(self, post_storage: PostStorage, presenter: JsonPresenter):
        self.post_storage = post_storage
        self.presenter = presenter

    def react_to_post(self, user_id: int, comment_id: int, reaction_type: str):
        comment_reaction_dto = self.post_storage.react_to_comment(user_id, comment_id, reaction_type)
        response = self.presenter.react_to_comment(comment_reaction_dto)
        return response
