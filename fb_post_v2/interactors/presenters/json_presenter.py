import abc

from fb_post_v2.interactors.storages.post_storage import PostDTO, GetPostDTO,\
    CommentDTO, PostReactionDTO, CommentReactionDTO, UserReactionDTO, \
    RepliesDTO, ReactionMetricDTO
from typing import List, Optional


class JsonPresenter:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_create_post_response(self, post_dto: PostDTO):
        pass

    @abc.abstractmethod
    def get_post_response(self, get_post_dto: GetPostDTO):
        pass

    @abc.abstractmethod
    def get_add_comment_to_post_response(self, comment_dto: CommentDTO):
        pass

    @abc.abstractmethod
    def get_add_reply_to_comment_response(self, comment_dto: CommentDTO):
        pass

    @abc.abstractmethod
    def get_react_to_post_response(
            self, post_reaction_dto: Optional[PostReactionDTO]):
        pass

    @abc.abstractmethod
    def get_react_to_comment_response(
            self, comment_reaction_dto: Optional[CommentReactionDTO]):
        pass

    @abc.abstractmethod
    def get_user_posts_response(self, user_posts_dto: List[GetPostDTO]):
        pass

    @abc.abstractmethod
    def get_posts_with_more_positive_reactions_response(
            self, post_ids: List[int]):
        pass

    @abc.abstractmethod
    def get_user_reacted_posts_response(self, post_ids: List[int]):
        pass

    @abc.abstractmethod
    def get_post_reactions_response(self, reactions_dto: List[UserReactionDTO]):
        pass

    @abc.abstractmethod
    def get_reaction_metrics_response(
            self, reaction_metrics_dto: List[ReactionMetricDTO]):
        pass

    @abc.abstractmethod
    def get_total_reaction_count_response(self, total_reactions_count: int):
        pass

    @abc.abstractmethod
    def get_comment_replies_response(self, replies_dto: List[RepliesDTO]):
        pass

    @abc.abstractmethod
    def raise_not_a_comment_exception(self):
        pass

    @abc.abstractmethod
    def get_delete_post_response(self):
        pass

    @abc.abstractmethod
    def raise_post_does_not_exist_exception(self):
        pass
