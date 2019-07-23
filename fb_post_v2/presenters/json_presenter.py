from typing import Dict, List, Optional

from django_swagger_utils.drf_server.exceptions import BadRequest
import datetime

from fb_post_v2.interactors.presenters.json_presenter import JsonPresenter
from fb_post_v2.interactors.storages.post_storage import RepliesDTO, TotalReactionsDTO, ReactionMetricDTO, \
    ReactionDetailsDTO, PostIdsDTO, GetPostDTO, CommentReactionDTO, PostReactionDTO, CommentDTO, PostDTO, UserDTO, \
    ReactionDataDTO, CommentDetailsDTOWithReplies


class JsonPresenter(JsonPresenter):

    def get_create_post_response(self, post_dto: PostDTO):
        response = {"post_id": post_dto.post_id}
        return response

    def get_formatted_date(self, datetime_object: datetime):
        return datetime_object.strftime('%y-%m-%d %H:%M:%S.%f')

    def get_user_response(self, user_dto: UserDTO):
        return {"user_id": user_dto.user_id, "name": user_dto.name, "profile_pic_url": user_dto.profile_pic_url}

    def get_reaction_response(self, reaction_dto: ReactionDataDTO):
        return {"count": reaction_dto.count, "type": reaction_dto.type}

    def get_comment_response(self, comment_dto):
        comment_data = {}
        comment_data['comment_id'] = comment_dto.comment_id
        comment_data['commenter'] = self.get_user_response(comment_dto.user)
        comment_data['commented_at'] = self.get_formatted_date(comment_dto.commented_at)
        comment_data['comment_content'] = comment_dto.comment_content
        comment_data['reactions'] = self.get_reaction_response(comment_dto.comment_reactions)

        return comment_data

    def get_comment_response_with_replies(self, comment_dto: CommentDetailsDTOWithReplies):
        comment_data = self.get_comment_response(comment_dto)

        comment_data['replies'] = []
        for reply_dto in comment_dto.replies:
            reply_data = self.get_comment_response(reply_dto)
            comment_data['replies'].append(reply_data)

        comment_data['replies_count'] = comment_dto.replies_count

        return comment_data

    def get_post_response(self, get_post_dto: GetPostDTO):

        post_data = {}
        post_data["post_id"] = get_post_dto.post_details.post_id
        post_data["posted_by"] = self.get_user_response(get_post_dto.posted_by)
        post_data["posted_at"] = self.get_formatted_date(get_post_dto.post_details.created_time)
        post_data["post_content"] = get_post_dto.post_details.post_content
        post_data["reactions"] = self.get_reaction_response(get_post_dto.post_reaction_data)

        post_data["comments"] = []
        for comment in get_post_dto.comments:
            comment_data = self.get_comment_response_with_replies(comment)
            post_data["comments"].append(comment_data)

        post_data["comments_count"] = get_post_dto.comments_count

        return post_data

    def get_add_comment_to_post_response(self, comment_dto: CommentDTO):
        response = {"comment_id": comment_dto.comment_id}
        return response

    def get_add_reply_to_comment_response(self, comment_dto: CommentDTO):
        response = {"reply_id": comment_dto.comment_id}
        return response

    def get_react_to_post_response(self, post_reaction_dto: Optional[PostReactionDTO]):

        if post_reaction_dto == None:
            response = {"status": "Reaction Deleted"}
        else:
            response = {"reaction_id": post_reaction_dto.reaction_id}
        return response

    def get_react_to_comment_response(self, comment_reaction_dto: Optional[CommentReactionDTO]):

        if comment_reaction_dto == None:
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

    def get_positive_posts_response(self, post_ids_dto: PostIdsDTO):
        response = {"post_ids": post_ids_dto.post_ids}
        return response

    def get_posts_reacted_by_user_response(self, post_ids_dto: PostIdsDTO):
        response = {"post_ids": post_ids_dto.post_ids}
        return response

    def get_reactions_to_post_response(self, reactions_dto: List[ReactionDetailsDTO]):

        reactions_list = []
        for reaction in reactions_dto:

            reaction_data = {}
            reaction_data['user_id'] = reaction.user_id
            reaction_data['name'] = reaction.name
            reaction_data['profile_pic'] = reaction.profile_pic_url
            reaction_data['reaction'] = reaction.reaction_type
            reactions_list.append(reaction_data)

        return reactions_list

    def get_reaction_metrics_response(self, reactions_metrics_dto: List[ReactionMetricDTO]):

        reaction_metrics_list = []
        for metric in reactions_metrics_dto:

            reaction_metric_data = {}
            reaction_metric_data['reaction_type'] = metric.reaction_type
            reaction_metric_data['count'] = metric.count
            reaction_metrics_list.append(reaction_metric_data)

        return reaction_metrics_list

    def get_total_reaction_count_response(self, total_reactions_dto: TotalReactionsDTO):
        response = {"count": total_reactions_dto.count}
        return response

    def get_replies_to_comment_response(self, replies_dto: List[RepliesDTO]):

        replies_list = []
        for reply in replies_dto:
            reply_data = {}
            reply_data['comment_id'] = reply.comment_id
            reply_data['commenter'] = self.get_user_response(reply.user)
            reply_data['commented_at'] = self.get_formatted_date(reply.commented_at)
            reply_data['comment_content'] = reply.comment_content
            replies_list.append(reply_data)

        return replies_list

    def raise_not_a_comment_exception(self):
        raise BadRequest(message='Invalid comment id', res_status='INVALID_COMMENT_ID')

    def get_delete_post_response(self):
        response = {"status": "Post Deleted"}
        return response

    def raise_post_does_not_exist_exception(self):
        raise BadRequest(message='Invalid post id', res_status='INVALID_POST_ID')
