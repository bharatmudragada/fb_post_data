from typing import List

from fb_post_v2.interactors.storages.post_storage import PostStorage, \
    RepliesDTO, UserReactionDTO, CommentReactionDTO, PostReactionDTO,\
    CommentDTO, GetPostDTO, PostDTO, ReactionMetricDTO, UserDTO,\
    CommentDetailsDTO, ReactionStatsDTO, CommentDetailsWithRepliesDTO

from fb_post_v2.models.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, F, Q, Subquery


class PostStorageImpl(PostStorage):

    def create_post(self, post_content: str, user_id: int) -> PostDTO:

        post = Post.objects.create(user_id=user_id, post_content=post_content)

        return PostDTO(
            post_id=post.id, user_id=post.user_id,
            post_content=post.post_content, created_time=post.posted_time)

    @staticmethod
    def convert_user_dict_to_dto(user):
        return UserDTO(user_id=user['user'], name=user['user__username'],
                       profile_pic_url=user['user__profile_pic_url'])

    @staticmethod
    def convert_reaction_stats_dict_to_dto(reaction_stats):
        return ReactionStatsDTO(
            count=reaction_stats['count'], type=list(reaction_stats['type']))

    def convert_comment_dict_to_comment_details_dto(
            self, comment, comment_reactions):

        user_dto = self.convert_user_dict_to_dto(comment)
        reaction_dto = self\
            .convert_reaction_stats_dict_to_dto(comment_reactions)

        comment_dto = CommentDetailsDTO(
            comment_id=comment['id'], user=user_dto,
            commented_at=comment['commented_time'],
            comment_content=comment['comment_text'],
            comment_reactions=reaction_dto)

        return comment_dto

    def convert_comment_dict_to_comment_details_with_replies_dto(
            self, comment, comment_reactions, replies, replies_count):

        user_dto = self.convert_user_dict_to_dto(comment)
        reaction_dto = self.convert_reaction_stats_dict_to_dto(comment_reactions)

        comment_dto = CommentDetailsWithRepliesDTO(
            comment_id=comment['id'], user=user_dto,
            commented_at=comment['commented_time'],
            comment_content=comment['comment_text'],
            comment_reactions=reaction_dto,
            replies=replies, replies_count=replies_count)

        return comment_dto

    @staticmethod
    def get_comment_wise_replies(all_comment_replies):
        comment_replies = {}

        for reply in all_comment_replies:
            try:
                comment_replies[reply['commented_on']].append(reply)
            except KeyError:
                comment_replies[reply['commented_on']] = [reply]

        return comment_replies

    @staticmethod
    def add_reaction_to_comment_reactions_dict(
            comment_reactions, reaction):
        try:
            comment_reaction = comment_reactions[reaction['comment_id']]
            comment_reaction['count'] += 1
            comment_reaction['type'].add(reaction['reaction_type'])
        except KeyError:
            comment_reactions[reaction['comment_id']] = \
                {"count": 1, "type": set([reaction['reaction_type']])}

    def get_comment_wise_reactions(self, all_comment_reactions):
        comment_reactions = {}

        for reaction in all_comment_reactions:
            self.add_reaction_to_comment_reactions_dict(
                comment_reactions, reaction)

        return comment_reactions

    @staticmethod
    def get_reply_reactions(comment_reactions, reply):
        try:
            reply_reactions = comment_reactions[reply['id']]
        except KeyError:
            reply_reactions = {"count": 0, "type": []}

        return reply_reactions

    def convert_comment_dict_to_comment_dto(
            self, all_comment_reactions, comment, replies_dto):

        if comment['id'] in all_comment_reactions:
            comment_reactions = all_comment_reactions[comment['id']]
        else:
            comment_reactions = {"count": 0, "type": {}}

        return self.convert_comment_dict_to_comment_details_with_replies_dto(
            comment, comment_reactions, replies_dto, len(replies_dto))

    def convert_comment_replies_dict_to_replies_dto_list(
            self, comment_replies, all_comment_reactions, comment):

        replies_dto = []
        for reply in comment_replies[comment['id']]:
            reply_reactions = self.get_reply_reactions(
                all_comment_reactions, reply)
            replies_dto.append(self.convert_comment_dict_to_comment_details_dto(
                reply, reply_reactions))

        return replies_dto

    def convert_comments_dict_to_comment_dto_list(
            self, comments_of_post, comment_replies, all_comment_reactions):
        all_comments_dto = []

        for comment in comments_of_post:
            replies_dto = []

            if comment['id'] in comment_replies:
                replies_dto = \
                    self.convert_comment_replies_dict_to_replies_dto_list(
                        comment_replies, all_comment_reactions, comment)

            all_comments_dto.append(self.convert_comment_dict_to_comment_dto(
                all_comment_reactions, comment, replies_dto))

        return all_comments_dto

    @staticmethod
    def retrieve_db_data_for_get_post(post):
        comments_of_post = Comment.objects.select_related('user')\
            .filter(post=post, commented_on=None)\
            .values('id', 'commented_on', 'user', 'user__username',
                    'user__profile_pic_url', 'comment_text', 'commented_time')

        comment_ids = comments_of_post.values('id')

        post_reactions = PostReactions.objects.filter(post=post)\
            .values_list('reaction_type', flat=True)

        post_reactions_count = post_reactions.count()
        post_reaction_types = list(post_reactions.distinct())

        all_comment_replies = Comment.objects.select_related('user')\
            .filter(commented_on__in=Subquery(comment_ids))\
            .values('id', 'commented_on', 'user', 'user__username',
                    'user__profile_pic_url', 'comment_text', 'commented_time')

        all_comment_ids = Comment.objects.filter(post=post).values('id')
        all_comment_reactions = CommentReactions.objects\
            .filter(comment_id__in=Subquery(all_comment_ids))\
            .values('comment_id', 'reaction_type')

        return comments_of_post, all_comment_replies,\
               all_comment_reactions, post_reactions_count, post_reaction_types

    def get_post(self, post_id: int) -> GetPostDTO:

        post = Post.objects.select_related('user').get(pk=post_id)

        comments_of_post, all_comment_replies, all_comment_reactions,\
        post_reactions_count, post_reaction_types = self\
            .retrieve_db_data_for_get_post(post)

        comment_replies = self.get_comment_wise_replies(all_comment_replies)

        comment_reactions = self.get_comment_wise_reactions(all_comment_reactions)

        comments_dto = self.convert_comments_dict_to_comment_dto_list(
            comments_of_post, comment_replies, comment_reactions)

        post_dto = PostDTO(
            post_id=post.id, user_id=post.user_id,
            post_content=post.post_content, created_time=post.posted_time)
        posted_user_dto = UserDTO(user_id=post.user_id, name=post.user.username,
                                  profile_pic_url=post.user.profile_pic_url)
        post_reactions_dto = ReactionStatsDTO(count=post_reactions_count,
                                              type=post_reaction_types)

        return GetPostDTO(
            post_details=post_dto, posted_by=posted_user_dto,
            post_reaction_data=post_reactions_dto, comments=comments_dto,
            comments_count=len(comments_dto))

    def add_comment_to_post(
            self, post_id: int, comment_user_id: int,
            comment_text: str) -> CommentDTO:

        comment = Comment.objects.create(
            post_id=post_id, commented_on=None, user_id=comment_user_id,
            comment_text=comment_text)

        return CommentDTO(
            comment_id=comment.id, user_id=comment.user_id,
            commented_at=comment.commented_time,
            comment_content=comment.comment_text,
            commented_on_id=comment.commented_on_id)

    def is_reply(self, comment_id: int) -> bool:

        comment = Comment.objects.get(pk=comment_id)

        if comment.commented_on is None:
            return False
        return True

    def get_comment_id_for_reply(self, comment_id: int) -> int:

        return Comment.objects.get(pk=comment_id).commented_on_id

    def add_reply_to_comment(self, comment_id: int,
                             reply_user_id: int, reply_text: str) -> CommentDTO:

        commented_on = Comment.objects.get(pk=comment_id)
        reply = Comment.objects.create(
            post_id=commented_on.post_id, commented_on=commented_on,
            user_id=reply_user_id, comment_text=reply_text)

        return CommentDTO(
            comment_id=reply.id, user_id=reply.user_id,
            commented_at=reply.commented_time,
            comment_content=reply.comment_text,
            commented_on_id=reply.commented_on_id)

    def post_reaction_exists(self, user_id: int, post_id: int) -> bool:

        try:
            PostReactions.objects.get(user_id=user_id, post_id=post_id)
            return True
        except ObjectDoesNotExist:
            return False

    def get_post_reaction(self, user_id: int, post_id: int) -> str:

        return PostReactions.objects\
            .get(user_id=user_id, post_id=post_id).reaction_type

    def delete_post_reaction(self, user_id: int, post_id: int):

        reaction = PostReactions.objects.get(user_id=user_id, post_id=post_id)
        reaction.delete()

    def update_post_reaction(
            self, user_id: int, post_id: int, reaction_type: str)\
            -> PostReactionDTO:

        reaction = PostReactions.objects.get(user_id=user_id, post_id=post_id)
        reaction.reaction_type = reaction_type
        reaction.save()

        return PostReactionDTO(
            reaction_id=reaction.id, user_id=reaction.user_id,
            reaction_type=reaction.reaction_type, post_id=reaction.post_id)

    def add_post_reaction(
            self, user_id: int, post_id: int, reaction_type: str)\
            -> PostReactionDTO:

        reaction = PostReactions.objects.create(
            post_id=post_id, user_id=user_id, reaction_type=reaction_type)

        return PostReactionDTO(
            reaction_id=reaction.id, user_id=reaction.user_id,
            reaction_type=reaction.reaction_type, post_id=reaction.post_id)

    def comment_reaction_exists(self, user_id: int, comment_id: int) -> bool:

        try:
            CommentReactions.objects.get(user_id=user_id, comment_id=comment_id)
            return True
        except ObjectDoesNotExist:
            return False

    def get_comment_reaction(self, user_id: int, comment_id: int) -> str:

        return CommentReactions.objects\
            .get(user_id=user_id, comment_id=comment_id).reaction_type

    def delete_comment_reaction(self, user_id: int, comment_id: int):

        reaction = CommentReactions.objects\
            .get(user_id=user_id, comment_id=comment_id)
        reaction.delete()

    def update_comment_reaction(
            self, user_id: int, comment_id: int, reaction_type: str)\
            -> CommentReactionDTO:

        reaction = CommentReactions.objects\
            .get(user_id=user_id, comment_id=comment_id)
        reaction.reaction_type = reaction_type
        reaction.save()

        return CommentReactionDTO(
            reaction_id=reaction.id, user_id=reaction.user_id,
            reaction_type=reaction.reaction_type, comment_id=reaction.comment_id)

    def add_comment_reaction(
            self, user_id: int, comment_id: int, reaction_type: str)\
            -> CommentReactionDTO:

        reaction = CommentReactions.objects.create(
            comment_id=comment_id, user_id=user_id, reaction_type=reaction_type)

        return CommentReactionDTO(
            reaction_id=reaction.id, user_id=reaction.user_id,
            reaction_type=reaction.reaction_type, comment_id=reaction.comment_id)

    def get_user_posts(self, user_id: int, offset: int, length: int)\
            -> List[GetPostDTO]:

        post_ids = list(Post.objects.filter(user__id=user_id)
                        .values_list('id', flat=True)[offset:offset + length])

        user_posts_data = []
        for post_id in post_ids:
            post_dto = self.get_post(post_id)
            user_posts_data.append(post_dto)

        return user_posts_data

    def get_posts_with_more_positive_reactions(self) -> List[int]:

        positive_reactions = Q(postreactions__reaction_type__in=
                               ['LIKE', 'LOVE', 'HAHA', 'WOW'])
        negative_reactions = Q(postreactions__reaction_type__in=['SAD', 'ANGRY'])

        count_positive_reactions = Count(
            'postreactions__reaction_type', filter=positive_reactions)

        count_negative_reactions = Count(
            'postreactions__reaction_type', filter=negative_reactions)

        post_ids = list(Post.objects.values('id')
                        .annotate(positiveCount=count_positive_reactions,
                                  negativeCount=count_negative_reactions)
                        .filter(positiveCount__gt=F('negativeCount'))
                        .values_list('id', flat=True))

        return post_ids

    def get_user_reacted_posts(self, user_id: int) -> List[int]:

        post_ids = list(PostReactions.objects.filter(user_id=user_id)
                        .values_list('post_id', flat=True))

        return post_ids

    def get_post_reactions(self, post_id: int, offset: int, length: int)\
            -> List[UserReactionDTO]:

        reactions = list(PostReactions.objects.filter(post_id=post_id)
                         .annotate(name=F('user__username'),
                                   profile_pic=F('user__profile_pic_url'),
                                   reaction=F('reaction_type'))
                         .values('user_id', 'name', 'profile_pic', 'reaction')
                         [offset:offset + length])

        reaction_details_list = []
        for reaction in reactions:
            reaction_dto = UserReactionDTO(
                user_id=reaction["user_id"], name=reaction["name"],
                profile_pic_url=reaction["profile_pic"],
                reaction_type=reaction["reaction"])
            reaction_details_list.append(reaction_dto)

        return reaction_details_list

    def get_reaction_metrics(self, post_id: int) -> List[ReactionMetricDTO]:

        post_reactions = PostReactions.objects.filter(post_id=post_id)\
            .values('reaction_type')\
            .annotate(reaction_count=Count('reaction_type'))

        reaction_metrics_dto = []
        for reaction in post_reactions:
            reaction_dto = ReactionMetricDTO(
                reaction_type=reaction['reaction_type'],
                count=reaction['reaction_count'])
            reaction_metrics_dto.append(reaction_dto)

        return reaction_metrics_dto

    def get_total_reaction_count(self) -> int:

        count = PostReactions.objects.count()

        return count

    @staticmethod
    def convert_reply_object_to_reply_dto(reply):
        user_dto = UserDTO(user_id=reply.user_id, name=reply.user.username,
                           profile_pic_url=reply.user.profile_pic_url)
        reply_dto = RepliesDTO(comment_id=reply.id, user=user_dto,
                               commented_at=reply.commented_time,
                               comment_content=reply.comment_text)
        return reply_dto

    def get_comment_replies(self, comment_id, offset, length)\
            -> List[RepliesDTO]:

        replies = Comment.objects.select_related('user').filter(
            commented_on=comment_id)[offset:offset + length]

        replies_dto = []
        for reply in replies:
            replies_dto.append(self.convert_reply_object_to_reply_dto(reply))

        return replies_dto

    def post_exists(self, post_id) -> bool:

        try:
            Post.objects.get(pk=post_id)
            return True
        except ObjectDoesNotExist:
            return False

    def delete_post(self, post_id):

        post = Post.objects.get(pk=post_id)
        post.delete()
