import json
from django.http.response import HttpResponse


class UpdateStatusCodeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        print("Before get response call")
        response = self.get_response(request)
        print("After get response call")

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print("In Process View")

    def process_exception(self, request, exception):
        print("In Process Exception")
        print("exception", type(exception))
        return HttpResponse(json.dumps({"status": "Invalid Request"}),
                            status=400)

    def process_template_response(self, request, response):
        print("In Process Template Response ")
        return response
