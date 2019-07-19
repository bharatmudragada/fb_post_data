from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import PostStorage


class ReactToPostInteractor:

    def __init__(self, post_storage: PostStorage, presenter: JsonPresenter):
        self.post_storage = post_storage
        self.presenter = presenter

    def react_to_post(self, user_id: int, post_id: int, reaction_type: str):
        post_reaction_exists = self.post_storage.post_reaction_exists(user_id, post_id)
        if post_reaction_exists:
            post_reaction = self.post_storage.get_post_reaction(user_id, post_id)
            if post_reaction == reaction_type:
                self.post_storage.delete_post_reaction(user_id, post_id)
                return self.presenter.delete_post_reaction()
            else:
                reaction_dto = self.post_storage.update_post_reaction(user_id, post_id, reaction_type)
                return self.presenter.update_post_reaction(reaction_dto)
        else:
            post_reaction_dto = self.post_storage.add_reaction_to_post(user_id, post_id, reaction_type)
            return self.presenter.add_reaction_to_post(post_reaction_dto)

