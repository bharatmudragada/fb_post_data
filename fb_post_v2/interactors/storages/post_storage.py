import abc
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict


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
class ReactionDataDTO:
    count: int
    type: [str]


@dataclass
class CommentDTO:
    comment_id: int
    commenter: UserDTO
    commented_at: datetime
    comment_content: str
    commented_on_id: int


@dataclass
class CommentDTOWithReactions(CommentDTO):
    reactions: ReactionDataDTO


@dataclass
class CommentDTOWithReplies(CommentDTOWithReactions):
    replies_count: 1
    replies: List[CommentDTOWithReactions]


@dataclass
class GetPostDTO:
    post_id: int
    posted_by: UserDTO
    posted_at: datetime
    post_content: str
    reactions: ReactionDataDTO
    comments: List[CommentDTOWithReplies]
    comments_count: int


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
class GetUserPostsDTO:
    posts: List[GetPostDTO]


@dataclass
class PostIdsDTO:
    post_ids: List[int]


@dataclass
class ReactionDetailsDTO(UserDTO):
    reaction_type: str


@dataclass
class ReactionMetricsDTO:
    metrics: List[Dict]


@dataclass
class TotalReactionsDTO:
    count: Dict[str, int]


class PostStorage:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create_post(self, post_content: str, user_id: int) -> PostDTO:
        pass

    @abc.abstractmethod
    def get_post(self, post_id: int) -> GetPostDTO:
        pass

    @abc.abstractmethod
    def add_comment_to_post(self, post_id: int, comment_user_id: int, comment_text: str) -> CommentDTO:
        pass

    @abc.abstractmethod
    def add_reply_to_comment(self, comment_id: int, reply_user_id: int, reply_text: str) -> CommentDTO:
        pass

    @abc.abstractmethod
    def react_to_post(self, user_id: int, post_id: int, reaction_type: str) -> PostReactionDTO:
        pass

    @abc.abstractmethod
    def react_to_comment(self, user_id: int, comment_id: int, reaction_type: str) -> CommentReactionDTO:
        pass

    @abc.abstractmethod
    def get_user_posts(self, user_id: int) -> GetUserPostsDTO:
        pass

    @abc.abstractmethod
    def get_positive_posts(self) -> PostIdsDTO:
        pass

    @abc.abstractmethod
    def get_posts_reacted_by_user(self, user_id: int) -> PostIdsDTO:
        pass

    @abc.abstractmethod
    def get_reactions_to_post(self, post_id: int) -> ReactionDetailsDTO:
        pass

    @abc.abstractmethod
    def get_reaction_metrics(self, post_id: int) -> ReactionMetricsDTO:
        pass

    @abc.abstractmethod
    def get_total_reaction_count(self) -> TotalReactionsDTO:
        pass

    @abc.abstractmethod
    def get_replies_to_comment(self, comment_id) -> List[CommentDTO]:
        pass

    @abc.abstractmethod
    def delete_post(self, post_id) -> Dict:
        pass