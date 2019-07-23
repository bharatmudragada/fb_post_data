from fb_post_v2.interactors.storages.post_storage import PostIdsDTO

from fb_post_v2.presenters.json_presenter import JsonPresenter


class TestGetPostsReactedByUserResponse:

    def test_get_posts_reacted_by_user_response(self):

        post_ids_dto = PostIdsDTO(post_ids=[1, 2, 3])

        json_presenter = JsonPresenter()
        response = json_presenter.get_posts_reacted_by_user_response(post_ids_dto)

        assert response["post_ids"] == post_ids_dto.post_ids
