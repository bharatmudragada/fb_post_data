from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator

from fb_post_v2.interactors.delete_post_interactor import DeletePostInteractor
from fb_post_v2.presenters.json_presenter import JsonPresenterImpl
from fb_post_v2.storages.post_storage import PostStorageImpl
from .validator_class import ValidatorClass
from django.http.response import HttpResponse
import json


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):

    post_id = kwargs["post_id"]

    post_storage = PostStorageImpl()
    json_presenter = JsonPresenterImpl()
    interactor = DeletePostInteractor(post_storage, json_presenter)

    response = interactor.delete_post(post_id)
    return HttpResponse(json.dumps(response), status=201)
