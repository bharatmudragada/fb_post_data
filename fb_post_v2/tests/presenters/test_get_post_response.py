import pytest
from freezegun import freeze_time

from fb_post_v2.interactors.storages.post_storage import GetPostDTO, PostDTO, UserDTO, ReactionDataDTO, \
    CommentDetailsDTO, CommentDetailsDTOWithReplies
import datetime

from fb_post_v2.presenters.json_presenter import JsonPresenter


class TestGetPostResponse:

    def setup_get_post_dto(self):
        post_dto = PostDTO(post_id=1, user_id=1, post_content='1', created_time=datetime.datetime.now())
        posted_user_dto = UserDTO(user_id=1, name='user_1', profile_pic_url='profile_pic')
        post_reaction_dto = ReactionDataDTO(count=1, type=['HAHA'])
        comments_dto_list = []
        comments_count = 2

        get_post_dto = GetPostDTO(post_details=post_dto, posted_by=posted_user_dto, post_reaction_data=post_reaction_dto, comments=comments_dto_list, comments_count=comments_count)

        return get_post_dto

    @freeze_time("2019-08-18")
    def test_get_post_response(self):

        get_post_dto = self.setup_get_post_dto()

        json_presenter = JsonPresenter()
        response = json_presenter.get_post_response(get_post_dto)

        assert response['post_id'] == get_post_dto.post_details.post_id
        assert response['posted_by']['user_id'] == get_post_dto.posted_by.user_id
        assert response['posted_by']['name'] == get_post_dto.posted_by.name
        assert response['posted_by']['profile_pic_url'] == get_post_dto.posted_by.profile_pic_url
        assert response['posted_at'] == get_post_dto.post_details.created_time.strftime('%y-%m-%d %H:%M:%S.%f')
        assert response['post_content'] == get_post_dto.post_details.post_content
        assert response['reactions']['count'] == get_post_dto.post_reaction_data.count
        assert response['reactions']['type'] == get_post_dto.post_reaction_data.type
        assert response['comments'] == get_post_dto.comments
        assert response['comments_count'] == get_post_dto.comments_count

    def test_get_user_response(self):

        user_dto = UserDTO(user_id=1, name='user_1', profile_pic_url='https://user_1.png')

        json_presenter = JsonPresenter()
        response = json_presenter.get_user_response(user_dto)

        assert response['user_id'] == user_dto.user_id
        assert response['name'] == user_dto.name
        assert response['profile_pic_url'] == user_dto.profile_pic_url

    def test_get_reaction_response(self):

        reaction_dto = ReactionDataDTO(count=1, type=["LOVE", "WOW"])

        json_presenter = JsonPresenter()
        response = json_presenter.get_reaction_response(reaction_dto)

        assert response['count'] == reaction_dto.count
        assert response['type'] == reaction_dto.type

    @freeze_time("2019-08-18")
    def test_get_comment_response(self):

        user_dto = UserDTO(user_id=1, name='user_1', profile_pic_url='https://user_1.png')
        comment_reactions_dto = ReactionDataDTO(count=3, type=["LOVE", "LIKE"])
        comment_dto = CommentDetailsDTO(comment_id=1, user=user_dto, commented_at=datetime.datetime.now(), comment_content="This is a comment", comment_reactions=comment_reactions_dto)

        json_presenter = JsonPresenter()
        response = json_presenter.get_comment_response(comment_dto)

        assert response['comment_id'] == comment_dto.comment_id
        assert response['commenter']['user_id'] == user_dto.user_id
        assert response['commenter']['name'] == user_dto.name
        assert response['commenter']['profile_pic_url'] == user_dto.profile_pic_url
        assert response['commented_at'] == comment_dto.commented_at.strftime('%y-%m-%d %H:%M:%S.%f')
        assert response['comment_content'] == comment_dto.comment_content
        assert response['reactions']['count'] == comment_reactions_dto.count
        assert response['reactions']['type'] == comment_reactions_dto.type

    @freeze_time("2019-08-18")
    def test_get_comment_response_with_replies(self):

        user_dto = UserDTO(user_id=1, name='user_1', profile_pic_url='https://user_1.png')
        comment_reactions_dto = ReactionDataDTO(count=2, type=["SAD", "LIKE"])
        reply_reactions_dto = ReactionDataDTO(count=3, type=["LOVE", "LIKE"])
        reply_dto = CommentDetailsDTO(comment_id=2, user=user_dto, commented_at=datetime.datetime.now(), comment_content="This is a reply", comment_reactions=reply_reactions_dto)
        comment_dto = CommentDetailsDTOWithReplies(comment_id=1, user=user_dto, commented_at=datetime.datetime.now(), comment_content="This is a comment", comment_reactions=comment_reactions_dto, replies=[reply_dto], replies_count=1)

        json_presenter = JsonPresenter()
        response = json_presenter.get_comment_response_with_replies(comment_dto)

        assert response['comment_id'] == comment_dto.comment_id
        assert response['commenter']['user_id'] == user_dto.user_id
        assert response['commenter']['name'] == user_dto.name
        assert response['commenter']['profile_pic_url'] == user_dto.profile_pic_url
        assert response['commented_at'] == comment_dto.commented_at.strftime('%y-%m-%d %H:%M:%S.%f')
        assert response['comment_content'] == comment_dto.comment_content
        assert response['reactions']['count'] == comment_reactions_dto.count
        assert response['reactions']['type'] == comment_reactions_dto.type
        assert response['replies_count'] == 1
        
        reply_data = None
        for reply in response["replies"]:
            if reply["comment_id"] == reply_dto.comment_id:
                reply_data = reply

        assert reply_data['comment_id'] == reply_dto.comment_id
        assert reply_data['commenter']['user_id'] == user_dto.user_id
        assert reply_data['commenter']['name'] == user_dto.name
        assert reply_data['commenter']['profile_pic_url'] == user_dto.profile_pic_url
        assert reply_data['commented_at'] == reply_dto.commented_at.strftime('%y-%m-%d %H:%M:%S.%f')
        assert reply_data['comment_content'] == reply_dto.comment_content
        assert reply_data['reactions']['count'] == reply_reactions_dto.count
        assert reply_data['reactions']['type'] == reply_reactions_dto.type
