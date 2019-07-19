from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class ReactToCommentInteractor:

    def __init__(self, post_storage: PostStorage, presenter: JsonPresenter):
        self.post_storage = post_storage
        self.presenter = presenter

    def react_to_comment(self, user_id: int, comment_id: int, reaction_type: str):
        comment_reaction_exists = self.post_storage.comment_reaction_exists(user_id, comment_id)
        if comment_reaction_exists:
            comment_reaction = self.post_storage.get_comment_reaction(user_id, comment_id)
            if comment_reaction == reaction_type:
                self.post_storage.delete_comment_reaction(user_id, comment_id)
                return self.presenter.delete_comment_reaction()
            else:
                reaction_dto = self.post_storage.update_comment_reaction(user_id, comment_id, reaction_type)
                return self.presenter.update_comment_reaction(reaction_dto)
        else:
            comment_reaction_dto = self.post_storage.add_reaction_to_comment(user_id, comment_id, reaction_type)
            return self.presenter.add_reaction_to_comment(comment_reaction_dto)
