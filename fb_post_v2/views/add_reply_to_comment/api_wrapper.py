from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator

from fb_post_v2.interactors.add_comment_interactor import AddCommentInteractor
from fb_post_v2.presenters.json_presenter import JsonPresenter
from fb_post_v2.storages.post_storage import PostStorage
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    comment_id = kwargs["comment_id"]
    user = kwargs["user"]
    request_data = kwargs["request_data"]

    post_storage = PostStorage()
    json_presenter = JsonPresenter()
    interactor = AddCommentInteractor(post_storage, json_presenter)

    response = interactor.add_reply_to_comment(comment_id, user.id, request_data["comment_text"])

    from django.http.response import HttpResponse
    import json
    return HttpResponse(json.dumps(response), status=201)