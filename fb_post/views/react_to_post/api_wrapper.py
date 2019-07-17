from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from .validator_class import ValidatorClass
from fb_post.Operations import react_to_post


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    post_id = kwargs["post_id"]
    request_data = kwargs["request_data"]
    user = kwargs["user"]

    react_to_post(user_id=user.id, post_id=post_id, reaction_type=request_data["reaction_type"])

    from django.http.response import HttpResponse
    return HttpResponse(status=201)