from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class ReactionInteractor:

    def __init__(self, post_storage: PostStorage, presenter: JsonPresenter):
        self.post_storage = post_storage
        self.presenter = presenter

    def react_to_comment(self, user_id: int, comment_id: int, reaction_type: str):
        comment_reaction_exists = self.post_storage.comment_reaction_exists(user_id, comment_id)

        if comment_reaction_exists:
            comment_reaction = self.post_storage.get_comment_reaction(user_id, comment_id)

            if comment_reaction == reaction_type:
                comment_reaction_dto = self.post_storage.delete_comment_reaction(user_id, comment_id)
            else:
                comment_reaction_dto = self.post_storage.update_comment_reaction(user_id, comment_id, reaction_type)

        else:
            comment_reaction_dto = self.post_storage.add_reaction_to_comment(user_id, comment_id, reaction_type)

        return self.presenter.get_react_to_comment_response(comment_reaction_dto)

    def react_to_post(self, user_id: int, post_id: int, reaction_type: str):
        post_reaction_exists = self.post_storage.post_reaction_exists(user_id, post_id)

        if post_reaction_exists:
            post_reaction = self.post_storage.get_post_reaction(user_id, post_id)

            if post_reaction == reaction_type:
                post_reaction_dto = self.post_storage.delete_post_reaction(user_id, post_id)
            else:
                post_reaction_dto = self.post_storage.update_post_reaction(user_id, post_id, reaction_type)

        else:
            post_reaction_dto = self.post_storage.add_reaction_to_post(user_id, post_id, reaction_type)

        return self.presenter.get_react_to_post_response(post_reaction_dto)
