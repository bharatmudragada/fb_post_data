from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from .validator_class import ValidatorClass
from fb_post.Operations import get_replies_for_comment
from django.core.exceptions import SuspiciousOperation


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    comment_id = kwargs["comment_id"]
    request_query_params = kwargs["request_query_params"]
    offset = request_query_params.offset
    limit = request_query_params.limit

    try:
        replies = get_replies_for_comment(comment_id=comment_id, offset=offset, limit=limit)

        from django.http.response import HttpResponse
        return HttpResponse(str(replies), status=201)
    except SuspiciousOperation:
        from django_swagger_utils.drf_server.exceptions import BadRequest
        raise BadRequest('Invalid comment id', 'INVALID_COMMENT_ID')
