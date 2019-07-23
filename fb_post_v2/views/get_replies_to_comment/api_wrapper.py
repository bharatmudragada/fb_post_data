from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator

from fb_post_v2.interactors.get_replies_to_comment_interactor import GetRepliesToCommentInteractor
from fb_post_v2.presenters.json_presenter import JsonPresenter
from fb_post_v2.storages.post_storage import PostStorage
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    comment_id = kwargs["comment_id"]
    request_query_params = kwargs["request_query_params"]
    offset = request_query_params.offset
    limit = request_query_params.limit

    post_storage = PostStorage()
    json_presenter = JsonPresenter()
    interactor = GetRepliesToCommentInteractor(post_storage, json_presenter)

    response = interactor.get_replies_to_comment(comment_id, offset, limit)

    from django.http.response import HttpResponse
    import json
    return HttpResponse(json.dumps(response), status=201)