import json
from typing import List, Optional

from django_swagger_utils.drf_server.exceptions import BadRequest
import datetime

from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import RepliesDTO, \
    ReactionMetricDTO, \
    UserReactionDTO, GetPostDTO, CommentReactionDTO, PostReactionDTO, \
    CommentDTO, PostDTO, UserDTO, \
    ReactionStatsDTO, CommentReactionStatsDTO

from collections import defaultdict


class JsonPresenterImpl(JsonPresenter):

    def get_create_post_response(self, post_dto: PostDTO):
        response = {"post_id": post_dto.post_id}
        return response

    @staticmethod
    def get_formatted_date(datetime_object: datetime):
        return datetime_object.strftime('%y-%m-%d %H:%M:%S.%f')

    @staticmethod
    def get_user_wise_user_dict(users_dto_list: List[UserDTO]):

        user_wise_user_dict = {}
        for user_dto in users_dto_list:
            user_dict = {
                "user_id": user_dto.user_id, "name": user_dto.name,
                "profile_pic_url": user_dto.profile_pic_url
            }
            user_wise_user_dict[user_dto.user_id] = user_dict

        return user_wise_user_dict

    @staticmethod
    def convert_reaction_stats_dto_to_dict(reaction_dto: ReactionStatsDTO):
        return {"count": reaction_dto.count, "type": reaction_dto.type}

    @staticmethod
    def get_comment_wise_comment_reaction_stats_dict(
            all_comment_reaction_stats: List[CommentReactionStatsDTO]):

        comments_wise_comment_reactions_dict = {}
        for comment_reaction_stats_dto in all_comment_reaction_stats:
            comment_reaction_stats_dict = {
                "count": comment_reaction_stats_dto.count,
                "type": comment_reaction_stats_dto.type
            }
            comments_wise_comment_reactions_dict[
                comment_reaction_stats_dto.comment_id] \
                = comment_reaction_stats_dict

        return comments_wise_comment_reactions_dict

    def convert_comment_dto_to_dict(
            self, comment_dto, user_dict, reaction_stats_dict):
        comment_dict = {
            "comment_id": comment_dto.comment_id,
            "commenter": user_dict,
            "commented_at": self.get_formatted_date(comment_dto.commented_at),
            "comment_content": comment_dto.comment_content,
            "reactions": reaction_stats_dict
        }
        return comment_dict

    @staticmethod
    def add_reply_to_all_comment_replies_dict(
            reply_dict, comment_wise_comment_replies_dict, commented_on_id):

        comment_replies = comment_wise_comment_replies_dict[commented_on_id]
        comment_replies.append(reply_dict)

        return comment_wise_comment_replies_dict

    @staticmethod
    def get_reaction_stats_dict(comment_wise_comment_reaction_stats, comment_id):

        try:
            reaction_stats_dict = \
                comment_wise_comment_reaction_stats[comment_id]
        except KeyError:
            reaction_stats_dict = {"count": 0, "type": []}

        return reaction_stats_dict

    def get_comment_wise_details_and_replies(
            self, all_comments, user_wise_user_dict, comment_wise_comment_dict):

        comment_wise_comments_dict = {}
        comment_wise_replies_dict = defaultdict(list)

        for comment_dto in all_comments:

            user_dict = user_wise_user_dict[comment_dto.user_id]
            reaction_stats_dict = self.get_reaction_stats_dict(
                comment_wise_comment_dict, comment_dto.comment_id)

            comment_dict = self.convert_comment_dto_to_dict(
                comment_dto, user_dict, reaction_stats_dict)

            if comment_dto.commented_on_id is None:
                comment_wise_comments_dict[comment_dto.comment_id] = comment_dict
            else:
                comment_wise_replies_dict = self\
                    .add_reply_to_all_comment_replies_dict(
                        comment_dict, comment_wise_replies_dict,
                        comment_dto.commented_on_id
                    )

        return comment_wise_comments_dict, comment_wise_replies_dict

    @staticmethod
    def add_replies_and_replies_count_to_comment_dict(
            comment_dict, replies_list):

        comment_dict['replies'] = replies_list
        comment_dict['replies_count'] = len(replies_list)
        return comment_dict

    def get_all_comment_details_list(
            self, all_comments, all_comment_reaction_stats, all_users_dict):

        comment_wise_comment_reaction_dict = \
            self.get_comment_wise_comment_reaction_stats_dict(
                all_comment_reaction_stats)

        comment_wise_comments_dict, comment_wise_comment_replies_dict = \
            self.get_comment_wise_details_and_replies(
                all_comments, all_users_dict, comment_wise_comment_reaction_dict)

        all_comment_details_list = []

        for comment_id in comment_wise_comments_dict:
            replies_list = comment_wise_comment_replies_dict[comment_id]

            comment_wise_comments_dict[comment_id] = \
                self.add_replies_and_replies_count_to_comment_dict(
                    comment_wise_comments_dict[comment_id], replies_list)

            all_comment_details_list.append(
                comment_wise_comments_dict[comment_id])

        return all_comment_details_list

    def get_post_response(self, get_post_dto: GetPostDTO):
        all_users_dict = self.\
            get_user_wise_user_dict(get_post_dto.users)

        post_data = {}
        post_details_dto = get_post_dto.post_details
        post_data["post_id"] = post_details_dto.post_id
        post_data["posted_by"] = all_users_dict[post_details_dto.user_id]
        post_data["posted_at"] = self\
            .get_formatted_date(post_details_dto.created_time)
        post_data["post_content"] = post_details_dto.post_content
        post_data["reactions"] = self\
            .convert_reaction_stats_dto_to_dict(get_post_dto.post_reaction_stats)

        post_data["comments"] = self.get_all_comment_details_list(
            get_post_dto.comments, get_post_dto.all_comment_reaction_stats,
            all_users_dict)

        post_data["comments_count"] = len(post_data["comments"])

        return post_data

    def get_add_comment_to_post_response(self, comment_dto: CommentDTO):
        response = {"comment_id": comment_dto.comment_id}
        return response

    def get_add_reply_to_comment_response(self, comment_dto: CommentDTO):
        response = {"reply_id": comment_dto.comment_id}
        return response

    def get_react_to_post_response(
            self, post_reaction_dto: Optional[PostReactionDTO]):

        if post_reaction_dto is None:
            response = {"status": "Reaction Deleted"}
        else:
            response = {"reaction_id": post_reaction_dto.reaction_id}
        return response

    def get_react_to_comment_response(
            self, comment_reaction_dto: Optional[CommentReactionDTO]):

        if comment_reaction_dto is None:
            response = {"status": "Reaction Deleted"}
        else:
            response = {"reaction_id": comment_reaction_dto.reaction_id}
        return response

    def get_user_posts_response(self, user_posts_dto: List[GetPostDTO]):

        user_posts_data = []
        for post_dto in user_posts_dto:
            post_data = self.get_post_response(post_dto)
            user_posts_data.append(post_data)

        return user_posts_data

    def get_posts_with_more_positive_reactions_response(
            self, post_ids: List[int]):
        response = {"post_ids": post_ids}
        return response

    def get_user_reacted_posts_response(self, post_ids: List[int]):
        response = {"post_ids": post_ids}
        return response

    @staticmethod
    def convert_reaction_dto_to_dict(reaction):
        reaction_data = {
            'user_id': reaction.user_id,
            'name': reaction.name,
            'profile_pic': reaction.profile_pic_url,
            'reaction': reaction.reaction_type
        }
        return reaction_data

    def get_post_reactions_response(self, reactions_dto: List[UserReactionDTO]):

        reactions_list = []
        for reaction in reactions_dto:
            reactions_list.append(self.convert_reaction_dto_to_dict(reaction))

        return reactions_list

    @staticmethod
    def convert_reaction_metric_dto_to_dict(reaction_metric):
        reaction_metric_dict = {
            'reaction_type': reaction_metric.reaction_type,
            'count': reaction_metric.count
        }
        return reaction_metric_dict

    def get_reaction_metrics_response(
            self, reactions_metrics_dto: List[ReactionMetricDTO]):

        reaction_metrics_list = []
        for reaction_metric in reactions_metrics_dto:
            reaction_metrics_list.append(
                self.convert_reaction_metric_dto_to_dict(reaction_metric))

        return reaction_metrics_list

    def get_total_reaction_count_response(self, total_reactions_count: int):
        response = {"count": total_reactions_count}
        return response

    @staticmethod
    def convert_user_dto_to_dict(user_dto: UserDTO):
        user_dict = {
            "user_id": user_dto.user_id,
            "name": user_dto.name,
            "profile_pic_url": user_dto.profile_pic_url
        }
        return user_dict

    def convert_reply_dto_to_dict(self, reply):
        reply_dict = {
            'comment_id': reply.comment_id,
            'commenter': self.convert_user_dto_to_dict(reply.user),
            'commented_at': self.get_formatted_date(reply.commented_at),
            'comment_content': reply.comment_content
        }
        return reply_dict

    def get_comment_replies_response(self, replies_dto: List[RepliesDTO]):

        replies_list = []
        for reply in replies_dto:
            replies_list.append(self.convert_reply_dto_to_dict(reply))

        return replies_list

    def raise_not_a_comment_exception(self):
        raise BadRequest(message='Invalid comment id',
                         res_status='INVALID_COMMENT_ID')

    def get_delete_post_response(self):
        response = {"status": "Post Deleted"}
        return response

    def raise_post_does_not_exist_exception(self):
        from django.core.exceptions import ObjectDoesNotExist
        raise ObjectDoesNotExist()
