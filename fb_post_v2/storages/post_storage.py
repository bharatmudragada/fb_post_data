from typing import Dict, List

from fb_post_v2.interactors.storages.post_storage import PostStorage, RepliesDTO, TotalReactionsDTO, \
    ReactionDetailsDTO, PostIdsDTO, CommentReactionDTO, PostReactionDTO, CommentDTO, GetPostDTO, \
    PostDTO, ReactionMetricDTO, UserDTO, CommentDetailsDTO, ReactionDataDTO, CommentDetailsDTOWithReplies

from fb_post_v2.models.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, F, Q, Subquery


class PostStorage(PostStorage):
    def create_post(self, post_content: str, user_id: int) -> PostDTO:

        post = Post.objects.create(user_id=user_id, post_content=post_content)

        return PostDTO(post_id=post.id, user_id=post.user_id, post_content=post.post_content, created_time=post.posted_time)

    def get_user_dto(self, comment):
        return UserDTO(user_id=comment['user'], name=comment['user__username'], profile_pic_url=comment['user__profile_pic_url'])

    def get_reaction_dto(self, comment_reactions):
        return ReactionDataDTO(count=comment_reactions['count'], type=list(comment_reactions['type']))

    def get_comment_dto(self, comment, comment_reactions):
        user_dto = self.get_user_dto(comment)
        reaction_dto = self.get_reaction_dto(comment_reactions)
        comment_dto = CommentDetailsDTO(comment_id=comment['id'], user=user_dto, commented_at=comment['commented_time'], comment_content=comment['comment_text'], comment_reactions=reaction_dto)
        return comment_dto

    def get_comment_dto_with_replies(self, comment, comment_reactions, replies, replies_count):
        user_dto = self.get_user_dto(comment)
        reaction_dto = self.get_reaction_dto(comment_reactions)
        comment_dto = CommentDetailsDTOWithReplies(comment_id=comment['id'], user=user_dto, commented_at=comment['commented_time'], comment_content=comment['comment_text'], comment_reactions=reaction_dto, replies=replies, replies_count=replies_count)
        return comment_dto

    def get_post(self, post_id: int) -> GetPostDTO:

        post = Post.objects.select_related('user').get(pk=post_id)

        comments_of_post = Comment.objects.select_related('user').filter(post=post, commented_on=None).values('id', 'commented_on', 'user', 'user__username', 'user__profile_pic_url', 'comment_text', 'commented_time')
        comment_ids = comments_of_post.values('id')

        post_reactions = PostReactions.objects.filter(post=post).values_list('reaction_type', flat=True)

        post_reactions_count = post_reactions.count()
        post_reaction_types = list(post_reactions.distinct())

        all_comment_replys = Comment.objects.select_related('user').filter(commented_on__in=Subquery(comment_ids)).values('id', 'commented_on', 'user', 'user__username', 'user__profile_pic_url', 'comment_text', 'commented_time')

        all_comment_ids = Comment.objects.filter(post=post).values('id')
        all_comment_reactions = CommentReactions.objects.filter(comment_id__in=Subquery(all_comment_ids)).values('comment_id', 'reaction_type')

        comment_replys = {}
        for reply in all_comment_replys:
            try:
                comment_replys[reply['commented_on']].append(reply)
            except KeyError:
                comment_replys[reply['commented_on']] = [reply]

        comment_reactions = {}
        for reaction in all_comment_reactions:
            try:
                comment_reaction = comment_reactions[reaction['comment_id']]
                comment_reaction['count'] += 1
                comment_reaction['type'].add(reaction['reaction_type'])
            except KeyError:
                comment_reactions[reaction['comment_id']] = {"count": 1, "type": set([reaction['reaction_type']])}

        comments_dto = []
        for comment in comments_of_post:
            replies_dto = []

            if comment['id'] in comment_replys:
                for reply in comment_replys[comment['id']]:
                    try:
                        reply_reactions = comment_reactions[reply['id']]
                    except KeyError:
                        reply_reactions = {"count": 0, "type": []}
                    replies_dto.append(self.get_comment_dto(reply, reply_reactions))

            if comment['id'] in comment_reactions:
                comments_dto.append(self.get_comment_dto_with_replies(comment, comment_reactions[comment['id']], replies_dto, len(replies_dto)))
            else:
                comments_dto.append(self.get_comment_dto_with_replies(comment, {"count": 0, "type": {}}, replies_dto, len(replies_dto)))

        post_dto = PostDTO(post_id=post.id, user_id=post.user_id, post_content=post.post_content, created_time=post.posted_time)
        posted_user_dto = UserDTO(user_id=post.user_id, name=post.user.username, profile_pic_url=post.user.profile_pic_url)
        post_reactions_dto = ReactionDataDTO(count=post_reactions_count, type=post_reaction_types)

        return GetPostDTO(post_details=post_dto, posted_by=posted_user_dto, post_reaction_data=post_reactions_dto, comments=comments_dto, comments_count=len(comments_dto))

    def add_comment_to_post(self, post_id: int, comment_user_id: int, comment_text: str) -> CommentDTO:

        comment = Comment.objects.create(post_id=post_id, commented_on=None, user_id=comment_user_id, comment_text=comment_text)

        return CommentDTO(comment_id=comment.id, user_id=comment.user_id, commented_at=comment.commented_time, comment_content=comment.comment_text, commented_on_id=comment.commented_on_id)

    def is_reply(self, comment_id: int) -> bool:

        comment = Comment.objects.get(pk=comment_id)

        if comment.commented_on == None:
            return False
        return True

    def get_comment_id_for_reply(self, comment_id: int) -> int:

        return Comment.objects.get(pk=comment_id).commented_on_id

    def add_reply_to_comment(self, comment_id: int, reply_user_id: int, reply_text: str) -> CommentDTO:

        commented_on = Comment.objects.get(pk=comment_id)
        reply = Comment.objects.create(post_id=commented_on.post_id, commented_on=commented_on, user_id=reply_user_id, comment_text=reply_text)

        return CommentDTO(comment_id=reply.id, user_id=reply.user_id, commented_at=reply.commented_time, comment_content=reply.comment_text, commented_on_id=reply.commented_on_id)

    def post_reaction_exists(self, user_id: int, post_id: int) -> bool:

        try:
            PostReactions.objects.get(user_id=user_id, post_id=post_id)
            return True
        except ObjectDoesNotExist:
            return False

    def get_post_reaction(self, user_id: int, post_id: int) -> str:

        return PostReactions.objects.get(user_id=user_id, post_id=post_id).reaction_type

    def delete_post_reaction(self, user_id: int, post_id: int):

        reaction = PostReactions.objects.get(user_id=user_id, post_id=post_id)
        reaction.delete()

    def update_post_reaction(self, user_id: int, post_id: int, reaction_type: str) -> PostReactionDTO:

        reaction = PostReactions.objects.get(user_id=user_id, post_id=post_id)
        reaction.reaction_type = reaction_type
        reaction.save()

        return PostReactionDTO(reaction_id=reaction.id, user_id=reaction.user_id, reaction_type=reaction.reaction_type, post_id=reaction.post_id)

    def add_reaction_to_post(self, user_id: int, post_id: int, reaction_type: str) -> PostReactionDTO:

        reaction = PostReactions.objects.create(post_id=post_id, user_id=user_id, reaction_type=reaction_type)

        return PostReactionDTO(reaction_id=reaction.id, user_id=reaction.user_id, reaction_type=reaction.reaction_type, post_id=reaction.post_id)

    def comment_reaction_exists(self, user_id: int, comment_id: int) -> bool:

        try:
            CommentReactions.objects.get(user_id=user_id, comment_id=comment_id)
            return True
        except ObjectDoesNotExist:
            return False

    def get_comment_reaction(self, user_id: int, comment_id: int) -> str:

        return CommentReactions.objects.get(user_id=user_id, comment_id=comment_id).reaction_type

    def delete_comment_reaction(self, user_id: int, comment_id: int):

        reaction = CommentReactions.objects.get(user_id=user_id, comment_id=comment_id)
        reaction.delete()

    def update_comment_reaction(self, user_id: int, comment_id: int, reaction_type: str) -> CommentReactionDTO:

        reaction = CommentReactions.objects.get(user_id=user_id, comment_id=comment_id)
        reaction.reaction_type = reaction_type
        reaction.save()

        return CommentReactionDTO(reaction_id=reaction.id, user_id=reaction.user_id, reaction_type=reaction.reaction_type, comment_id=reaction.comment_id)

    def add_reaction_to_comment(self, user_id: int, comment_id: int, reaction_type: str) -> CommentReactionDTO:

        reaction = CommentReactions.objects.create(comment_id=comment_id, user_id=user_id, reaction_type=reaction_type)

        return CommentReactionDTO(reaction_id=reaction.id, user_id=reaction.user_id, reaction_type=reaction.reaction_type, comment_id=reaction.comment_id)

    def get_user_posts(self, user_id: int, offset: int, length: int) -> List[GetPostDTO]:

        post_ids = list(Post.objects.filter(user__id=user_id).values_list('id', flat=True)[offset:offset + length])

        user_posts_data = []
        for post_id in post_ids:
            post_dto = self.get_post(post_id)
            user_posts_data.append(post_dto)

        return user_posts_data

    def get_positive_posts(self) -> PostIdsDTO:

        post_ids = list(Post.objects.values('id').annotate(positiveCount=Count('postreactions__reaction_type', filter=Q(postreactions__reaction_type__in=['LIKE', 'LOVE', 'HAHA', 'WOW'])), negativeCount=Count('postreactions__reaction_type', filter=Q(postreactions__reaction_type__in=['SAD', 'ANGRY']))).filter(positiveCount__gt=F('negativeCount')).values_list('id', flat=True))

        return PostIdsDTO(post_ids=post_ids)

    def get_posts_reacted_by_user(self, user_id: int) -> PostIdsDTO:

        post_ids = list(PostReactions.objects.filter(user_id=user_id).values_list('post_id', flat=True))

        return PostIdsDTO(post_ids=post_ids)

    def get_reactions_to_post(self, post_id: int, offset: int, length: int) -> List[ReactionDetailsDTO]:

        reactions = list(PostReactions.objects.filter(post_id=post_id).annotate(name=F('user__username'), profile_pic=F('user__profile_pic_url'), reaction=F('reaction_type')).values('user_id', 'name', 'profile_pic', 'reaction')[offset:offset + length])

        reaction_details_list = []
        for reaction in reactions:
            reaction_dto = ReactionDetailsDTO(user_id=reaction["user_id"], name=reaction["name"], profile_pic_url=reaction["profile_pic"], reaction_type=reaction["reaction"])
            reaction_details_list.append(reaction_dto)

        return reaction_details_list

    def get_reaction_metrics(self, post_id: int) -> List[ReactionMetricDTO]:

        post_reactions = PostReactions.objects.filter(post_id=post_id).values('reaction_type').annotate(reaction_count=Count('reaction_type'))

        reaction_metrics_dto = []
        for reaction in post_reactions:
            reaction_dto = ReactionMetricDTO(reaction_type=reaction['reaction_type'], count=reaction['reaction_count'])
            reaction_metrics_dto.append(reaction_dto)

        return reaction_metrics_dto

    def get_total_reaction_count(self) -> TotalReactionsDTO:

        count = PostReactions.objects.count()

        return TotalReactionsDTO(count=count)

    def get_replies_to_comment(self, comment_id, offset, length) -> List[RepliesDTO]:

        replies = Comment.objects.select_related('user').filter(commented_on=comment_id)[offset:offset + length]

        replies_dto = []
        for reply in replies:
            user_dto = UserDTO(user_id=reply.user_id, name=reply.user.username, profile_pic_url=reply.user.profile_pic_url)
            reply_dto = RepliesDTO(comment_id=reply.id, user=user_dto, commented_at=reply.commented_time, comment_content=reply.comment_text)
            replies_dto.append(reply_dto)

        return replies_dto

    def post_exists(self, post_id) -> bool:

        try:
            Post.objects.get(pk=post_id)
            return True
        except ObjectDoesNotExist:
            return False

    def delete_post(self, post_id) -> Dict:

        post = Post.objects.get(pk=post_id)
        post.delete()

        return {"status": "Post Deleted"}
