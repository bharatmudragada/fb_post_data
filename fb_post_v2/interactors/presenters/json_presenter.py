import abc

from fb_post_v2.interactors.storages.post_storage import PostDTO, GetPostDTO, CommentDTO, PostReactionDTO, \
    CommentReactionDTO, GetUserPostsDTO, PostIdsDTO, ReactionDetailsDTO, ReactionMetricsDTO, TotalReactionsDTO
from typing import List, Dict, Optional


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
    def get_react_to_post_response(self, post_reaction_dto: Optional[PostReactionDTO]):
        pass

    @abc.abstractmethod
    def get_react_to_comment_response(self, comment_reaction_dto: Optional[CommentReactionDTO]):
        pass

    @abc.abstractmethod
    def get_user_posts_response(self, user_posts_dto: GetUserPostsDTO):
        pass

    @abc.abstractmethod
    def get_positive_posts_response(self, post_ids_dto: PostIdsDTO):
        pass

    @abc.abstractmethod
    def get_posts_reacted_by_user_response(self, post_ids_dto: PostIdsDTO):
        pass

    @abc.abstractmethod
    def get_reactions_to_post_response(self, reactions_dto: ReactionDetailsDTO):
        pass

    @abc.abstractmethod
    def get_reaction_metrics_response(self, reactions_dto: ReactionMetricsDTO):
        pass

    @abc.abstractmethod
    def get_total_reaction_count_response(self, reactions_dto: TotalReactionsDTO):
        pass

    @abc.abstractmethod
    def get_replies_to_comment_response(self, replies_dto: List[CommentDTO]):
        pass

    @abc.abstractmethod
    def raise_not_a_comment_exception(self):
        pass

    @abc.abstractmethod
    def get_delete_post_response(self, status_dict: Dict):
        pass

    @abc.abstractmethod
    def raise_post_does_not_exist_exception(self):
        pass
