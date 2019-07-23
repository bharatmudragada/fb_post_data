from freezegun import freeze_time
from fb_post_v2.interactors.storages.post_storage import RepliesDTO, UserDTO
from datetime import datetime

from fb_post_v2.presenters.json_presenter import JsonPresenter


class TestGetRepliesToCommentResponse:

    @freeze_time("2019-08-18")
    def test_get_replies_to_comment(self):

        user_one_dto = UserDTO(user_id=1, name='user_1', profile_pic_url='https://user_1.png')
        user_two_dto = UserDTO(user_id=2, name='user_2', profile_pic_url='https://user_2.png')
        reply_one_dto = RepliesDTO(comment_id=1, user=user_one_dto, commented_at=datetime.now(), comment_content="This is first reply")
        reply_two_dto = RepliesDTO(comment_id=2, user=user_two_dto, commented_at=datetime.now(), comment_content="This is second reply")
        replies_dto_list = [reply_one_dto, reply_two_dto]

        json_presenter = JsonPresenter()
        response = json_presenter.get_replies_to_comment_response(replies_dto_list)

        reply_one_data = None
        for reply in response:
            if reply['comment_id'] == reply_one_dto.comment_id:
                reply_one_data = reply

        assert reply_one_data['commenter']['user_id'] == user_one_dto.user_id
        assert reply_one_data['commenter']['name'] == user_one_dto.name
        assert reply_one_data['commenter']['profile_pic_url'] == user_one_dto.profile_pic_url
        assert reply_one_data['commented_at'] == reply_one_dto.commented_at.strftime('%y-%m-%d %H:%M:%S.%f')
        assert reply_one_data['comment_content'] == reply_one_dto.comment_content

        reply_two_data = None
        for reply in response:
            if reply['comment_id'] == reply_two_dto.comment_id:
                reply_two_data = reply

        assert reply_two_data['commenter']['user_id'] == user_two_dto.user_id
        assert reply_two_data['commenter']['name'] == user_two_dto.name
        assert reply_two_data['commenter']['profile_pic_url'] == user_two_dto.profile_pic_url
        assert reply_two_data['commented_at'] == reply_two_dto.commented_at.strftime('%y-%m-%d %H:%M:%S.%f')
        assert reply_two_data['comment_content'] == reply_two_dto.comment_content
