from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator

from fb_post_v2.interactors.create_post_interactor import CreatePostInteractor
from fb_post_v2.presenters.json_presenter import JsonPresenterImpl
from fb_post_v2.storages.post_storage import PostStorageImpl
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):

    request_data = kwargs["request_data"]
    user = kwargs["user"]

    post_storage = PostStorageImpl()
    json_presenter = JsonPresenterImpl()
    interactor = CreatePostInteractor(post_storage, json_presenter)

    response = interactor.create_post(request_data["post_content"], user.id)

    from django.http.response import HttpResponse
    import json
    return HttpResponse(json.dumps(response), status=201)
