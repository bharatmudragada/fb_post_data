from fb_post_v2.interactors.storages.post_storage import UserReactionDTO

from fb_post_v2.presenters.json_presenter import JsonPresenterImpl


class TestGetReactionsToPostResponse:

    def test_get_reactions_to_post_response(self):

        reactions_dto_one = UserReactionDTO(
            user_id=1, name='user_1', profile_pic_url='https://user_1.png',
            reaction_type="LOVE")
        reactions_dto_two = UserReactionDTO(
            user_id=2, name='user_2', profile_pic_url='https://user_2.png',
            reaction_type="LIKE")
        reaction_dto_list = [reactions_dto_one, reactions_dto_two]

        json_presenter = JsonPresenterImpl()
        response = json_presenter.get_post_reactions_response(reaction_dto_list)

        reaction_one_data = None
        for reaction in response:
            if reaction['user_id'] == reactions_dto_one.user_id:
                reaction_one_data = reaction

        assert reaction_one_data['name'] == reactions_dto_one.name
        assert reaction_one_data['profile_pic'] == reactions_dto_one\
            .profile_pic_url
        assert reaction_one_data['reaction'] == reactions_dto_one.reaction_type

        reaction_two_data = None
        for reaction in response:
            if reaction['user_id'] == reactions_dto_two.user_id:
                reaction_two_data = reaction

        assert reaction_two_data['name'] == reactions_dto_two.name
        assert reaction_two_data['profile_pic'] == reactions_dto_two\
            .profile_pic_url
        assert reaction_two_data['reaction'] == reactions_dto_two.reaction_type
