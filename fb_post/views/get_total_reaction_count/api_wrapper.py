from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from .validator_class import ValidatorClass
from fb_post.Operations import get_total_reaction_count


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    count = get_total_reaction_count()

    response = {"count": count}

    from django.http.response import HttpResponse
    return HttpResponse(str(response), status=201)