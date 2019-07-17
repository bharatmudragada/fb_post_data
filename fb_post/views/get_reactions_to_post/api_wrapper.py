from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from .validator_class import ValidatorClass
from fb_post.Operations import get_reactions_to_post


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    post_id = kwargs["post_id"]
    request_query_params = kwargs["request_query_params"]
    offset = request_query_params.offset
    limit = request_query_params.limit

    reactions = get_reactions_to_post(post_id=post_id, offset=offset, limit=limit)

    from django.http.response import HttpResponse
    return HttpResponse(str(reactions), status=201)