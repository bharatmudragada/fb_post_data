from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator

from fb_post_v2.interactors.reaction_interactor import ReactionInteractor
from fb_post_v2.presenters.json_presenter import JsonPresenter
from fb_post_v2.storages.post_storage import PostStorage
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    post_id = kwargs["post_id"]
    request_data = kwargs["request_data"]

    post_storage = PostStorage()
    json_presenter = JsonPresenter()
    interactor = ReactionInteractor(post_storage, json_presenter)

    response = interactor.react_to_post(user.id, post_id, request_data["reaction_type"])

    from django.http.response import HttpResponse
    import json
    return HttpResponse(json.dumps(response), status=201)
