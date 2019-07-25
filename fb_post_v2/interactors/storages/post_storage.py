import abc
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class PostDTO:
    post_id: int
    user_id: int
    post_content: str
    created_time: datetime


@dataclass
class UserDTO:
    user_id: int
    name: str
    profile_pic_url: str


@dataclass
class ReactionStatsDTO:
    count: int
    type: List[str]


@dataclass
class CommentDTO:
    comment_id: int
    user_id: int
    commented_at: datetime
    comment_content: str
    commented_on_id: Optional[int]


@dataclass
class ReactionDTO:
    reaction_id: int
    user_id: int
    reaction_type: str


@dataclass
class PostReactionDTO(ReactionDTO):
    post_id: int


@dataclass
class CommentReactionDTO(ReactionDTO):
    comment_id: int


@dataclass
class CommentReactionStatsDTO(ReactionStatsDTO):
    comment_id: int


@dataclass
class GetPostDTO:
    post_details: PostDTO
    post_reaction_stats: ReactionStatsDTO
    comments: List[CommentDTO]
    all_comment_reaction_stats: List[CommentReactionStatsDTO]
    users: List[UserDTO]


@dataclass
class UserReactionDTO(UserDTO):
    reaction_type: str


@dataclass
class ReactionMetricDTO:
    reaction_type: str
    count: int


@dataclass
class RepliesDTO:
    comment_id: int
    user: UserDTO
    commented_at: datetime
    comment_content: str


class PostStorage:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create_post(self, post_content: str, user_id: int) -> PostDTO:
        pass

    @abc.abstractmethod
    def get_post(self, post_id: int) -> GetPostDTO:
        pass

    @abc.abstractmethod
    def add_comment_to_post(self, post_id: int, comment_user_id: int,
                            comment_text: str) -> CommentDTO:
        pass

    @abc.abstractmethod
    def is_reply(self, comment_id: int) -> bool:
        pass

    @abc.abstractmethod
    def get_comment_id_for_reply(self, reply_id: int) -> int:
        pass

    @abc.abstractmethod
    def add_reply_to_comment(self, comment_id: int, reply_user_id: int,
                             reply_text: str) -> CommentDTO:
        pass

    @abc.abstractmethod
    def post_reaction_exists(self, user_id: int, post_id: int) -> bool:
        pass

    @abc.abstractmethod
    def get_post_reaction(self, user_id: int, post_id: int) -> str:
        pass

    @abc.abstractmethod
    def delete_post_reaction(self, user_id: int, post_id: int):
        pass

    @abc.abstractmethod
    def update_post_reaction(self, user_id: int, post_id: int,
                             reaction_type: str) -> PostReactionDTO:
        pass

    @abc.abstractmethod
    def add_post_reaction(self, user_id: int, post_id: int,
                          reaction_type: str) -> PostReactionDTO:
        pass

    @abc.abstractmethod
    def comment_reaction_exists(self, user_id: int, comment_id: int) -> bool:
        pass

    @abc.abstractmethod
    def get_comment_reaction(self, user_id: int, comment_id: int) -> str:
        pass

    @abc.abstractmethod
    def delete_comment_reaction(self, user_id: int, comment_id: int):
        pass

    @abc.abstractmethod
    def update_comment_reaction(self, user_id: int, comment_id: int,
                                reaction_type: str) -> CommentReactionDTO:
        pass

    @abc.abstractmethod
    def add_comment_reaction(self, user_id: int, comment_id: int,
                             reaction_type: str) -> CommentReactionDTO:
        pass

    @abc.abstractmethod
    def get_user_posts(self, user_id: int, offset: int,
                       length: int) -> List[GetPostDTO]:
        pass

    @abc.abstractmethod
    def get_posts_with_more_positive_reactions(self) -> List[int]:
        pass

    @abc.abstractmethod
    def get_user_reacted_posts(self, user_id: int) -> List[int]:
        pass

    @abc.abstractmethod
    def get_post_reactions(self, post_id: int, offset: int,
                           length: int) -> List[UserReactionDTO]:
        pass

    @abc.abstractmethod
    def get_reaction_metrics(self, post_id: int) -> List[ReactionMetricDTO]:
        pass

    @abc.abstractmethod
    def get_total_reaction_count(self) -> int:
        pass

    @abc.abstractmethod
    def get_comment_replies(self, comment_id, offset,
                            length) -> List[RepliesDTO]:
        pass

    @abc.abstractmethod
    def post_exists(self, post_id) -> bool:
        pass

    @abc.abstractmethod
    def delete_post(self, post_id):
        pass
