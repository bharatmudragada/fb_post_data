from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from .validator_class import ValidatorClass
from fb_post.Operations import reply_to_comment


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    comment_id = kwargs["comment_id"]
    request_data = kwargs["request_data"]

    reply_id = reply_to_comment(reply_user_id=user.id, comment_id=comment_id, reply_text=request_data["comment_text"])

    response = {"reply_comment_id": reply_id}

    from django.http.response import HttpResponse
    return HttpResponse(str(response), status=201)
