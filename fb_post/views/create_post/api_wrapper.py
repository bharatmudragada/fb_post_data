from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from .validator_class import ValidatorClass
from fb_post.Operations import create_post


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    request_data = kwargs["request_data"]

    post_id = create_post(user_id=user.id, post_content=request_data["post_content"])

    response = {"post_id": post_id}

    from django.http.response import HttpResponse
    return HttpResponse(str(response), status=201)
