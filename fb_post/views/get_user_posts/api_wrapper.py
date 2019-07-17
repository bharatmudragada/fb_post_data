from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from .validator_class import ValidatorClass
from fb_post.Operations import get_user_posts, get_post

@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):

    user = kwargs["user"]
    request_query_params = kwargs["request_query_params"]
    offset = request_query_params.offset
    limit = request_query_params.limit

    post_ids = get_user_posts(user_id=user.id, offset=offset, limit=limit)

    response = []
    for id in post_ids:
        response.append(get_post(post_id=id))

    from django.http.response import HttpResponse
    return HttpResponse(str(response), status=201)