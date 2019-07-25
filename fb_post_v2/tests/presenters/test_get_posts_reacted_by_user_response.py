from fb_post_v2.presenters.json_presenter import JsonPresenterImpl


class TestGetPostsReactedByUserResponse:

    def test_get_posts_reacted_by_user_response(self):

        post_ids = [1, 2, 3]

        json_presenter = JsonPresenterImpl()
        response = json_presenter.get_user_reacted_posts_response(post_ids)

        assert response["post_ids"] == post_ids
