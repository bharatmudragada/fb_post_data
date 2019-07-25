from fb_post_v2.presenters.json_presenter import JsonPresenterImpl


class TestGetPositivePostsResponse:

    def test_get_positive_posts_response(self):

        post_ids = [1, 2, 3]

        json_presenter = JsonPresenterImpl()
        response = json_presenter\
            .get_posts_with_more_positive_reactions_response(post_ids)

        assert response["post_ids"] == post_ids
