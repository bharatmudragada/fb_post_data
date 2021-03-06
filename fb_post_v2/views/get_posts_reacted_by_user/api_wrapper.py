from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator

from fb_post_v2.interactors.get_posts_reacted_by_user_interactor\
    import GetUserReactedPostsInteractor
from fb_post_v2.presenters.json_presenter import JsonPresenterImpl
from fb_post_v2.storages.post_storage import PostStorageImpl
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    user = kwargs["user"]

    post_storage = PostStorageImpl()
    json_presenter = JsonPresenterImpl()
    interactor = GetUserReactedPostsInteractor(post_storage, json_presenter)

    response = interactor.get_posts_reacted_by_user(user.id)

    from django.http.response import HttpResponse
    import json
    return HttpResponse(json.dumps(response), status=201)
