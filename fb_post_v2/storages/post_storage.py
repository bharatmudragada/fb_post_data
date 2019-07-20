from typing import Dict, List

from fb_post_v2.interactors.storages.post_storage import PostStorage, CommentDTO, TotalReactionsDTO, ReactionMetricsDTO, \
    ReactionDetailsDTO, PostIdsDTO, GetUserPostsDTO, CommentReactionDTO, PostReactionDTO, GetPostDTO, PostDTO

from fb_post_v2.models.models import *


class PostStorage(PostStorage):
    def create_post(self, post_content: str, user_id: int) -> PostDTO:
        pass

    def get_post(self, post_id: int) -> GetPostDTO:
        pass

    def add_comment_to_post(self, post_id: int, comment_user_id: int, comment_text: str) -> CommentDTO:
        pass

    def is_comment(self, comment_id: int) -> bool:
        pass

    def get_comment_id(self, comment_id: int) -> int:
        pass

    def add_reply_to_comment(self, comment_id: int, reply_user_id: int, reply_text: str) -> CommentDTO:
        pass

    def post_reaction_exists(self, user_id: int, post_id: int) -> bool:
        pass

    def get_post_reaction(self, user_id: int, post_id: int) -> str:
        pass

    def delete_post_reaction(self, user_id: int, post_id: int):
        pass

    def update_post_reaction(self, user_id: int, post_id: int, reaction_type: str) -> PostReactionDTO:
        pass

    def add_reaction_to_post(self, user_id: int, post_id: int, reaction_type: str) -> PostReactionDTO:
        pass

    def comment_reaction_exists(self, user_id: int, post_id: int) -> bool:
        pass

    def get_comment_reaction(self, user_id: int, comment_id: int) -> str:
        pass

    def delete_comment_reaction(self, user_id: int, comment_id: int):
        pass

    def update_comment_reaction(self, user_id: int, comment_id: int, reaction_type: str) -> CommentReactionDTO:
        pass

    def add_reaction_to_comment(self, user_id: int, comment_id: int, reaction_type: str) -> CommentReactionDTO:
        pass

    def get_user_posts(self, user_id: int) -> GetUserPostsDTO:
        pass

    def get_positive_posts(self) -> PostIdsDTO:
        pass

    def get_posts_reacted_by_user(self, user_id: int) -> PostIdsDTO:
        pass

    def get_reactions_to_post(self, post_id: int) -> ReactionDetailsDTO:
        pass

    def get_reaction_metrics(self, post_id: int) -> ReactionMetricsDTO:
        pass

    def get_total_reaction_count(self) -> TotalReactionsDTO:
        pass

    def get_replies_to_comment(self, comment_id) -> List[CommentDTO]:
        pass

    def post_exists(self, post_id) -> bool:
        pass

    def delete_post(self, post_id) -> Dict:
        pass