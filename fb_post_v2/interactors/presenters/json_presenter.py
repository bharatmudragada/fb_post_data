import abc

from fb_post_v2.interactors.storages.post_storage import PostDTO, GetPostDTO, CommentDTO, PostReactionDTO, \
    CommentReactionDTO, GetUserPostsDTO, PostIdsDTO, ReactionDetailsDTO, ReactionMetricsDTO, TotalReactionsDTO
from typing import List, Dict


class JsonPresenter:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create_post(self, post_dto: PostDTO):
        pass

    @abc.abstractmethod
    def get_post(self, get_post_dto: GetPostDTO):
        pass

    @abc.abstractmethod
    def add_comment_to_post(self, comment_dto: CommentDTO):
        pass

    @abc.abstractmethod
    def add_reply_to_comment(self, comment_dto: CommentDTO):
        pass

    @abc.abstractmethod
    def react_to_post(self, post_reaction_dto: PostReactionDTO):
        pass

    @abc.abstractmethod
    def react_to_comment(self, comment_reaction_dto: CommentReactionDTO):
        pass

    @abc.abstractmethod
    def get_user_posts(self, user_posts_dto: GetUserPostsDTO):
        pass

    @abc.abstractmethod
    def get_positive_posts(self, post_ids_dto: PostIdsDTO):
        pass

    @abc.abstractmethod
    def get_posts_reacted_by_user(self, post_ids_dto: PostIdsDTO):
        pass

    @abc.abstractmethod
    def get_reactions_to_post(self, reactions_dto: ReactionDetailsDTO):
        pass

    @abc.abstractmethod
    def get_reaction_metrics(self, reactions_dto: ReactionMetricsDTO):
        pass

    @abc.abstractmethod
    def get_total_reaction_count(self, reactions_dto: TotalReactionsDTO):
        pass

    @abc.abstractmethod
    def get_replies_to_comment(self, replies_dto: List[CommentDTO]):
        pass

    @abc.abstractmethod
    def delete_post(self, status_dict: Dict):
        pass

