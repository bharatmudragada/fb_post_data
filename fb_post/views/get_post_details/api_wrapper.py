from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from .validator_class import ValidatorClass
from fb_post.Operations import get_post


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    post_id = kwargs["post_id"]

    print(post_id)

    response = get_post(post_id=post_id)

    print(response)

    from django.http.response import HttpResponse
    return HttpResponse(str(response), status=201)
