from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from .validator_class import ValidatorClass
from fb_post.Operations import get_posts_with_more_positive_reactions


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    post_ids = get_posts_with_more_positive_reactions()

    response = {"post_ids": post_ids}

    from django.http.response import HttpResponse
    return HttpResponse(str(response), status=201)