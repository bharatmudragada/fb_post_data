from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator

from fb_post_v2.interactors.get_positive_posts_interactor import GetPositivePostsInteractor
from fb_post_v2.presenters.json_presenter import JsonPresenter
from fb_post_v2.storages.post_storage import PostStorage
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):

    post_storage = PostStorage()
    json_presenter = JsonPresenter()
    interactor = GetPositivePostsInteractor(post_storage, json_presenter)

    response = interactor.get_positive_posts()

    from django.http.response import HttpResponse
    import json
    return HttpResponse(json.dumps(response), status=201)