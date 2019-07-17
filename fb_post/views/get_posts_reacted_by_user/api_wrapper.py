from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from .validator_class import ValidatorClass
from fb_post.Operations import get_posts_reacted_by_user


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    user = kwargs["user"]

    post_ids = get_posts_reacted_by_user(user_id=user.id)

    response = {"post_ids": post_ids}

    from django.http.response import HttpResponse
    return HttpResponse(str(response), status=201)