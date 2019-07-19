from django.apps import AppConfig


class FbPostV2AppConfig(AppConfig):
    name = "fb_post_v2"

    def ready(self):
        from fb_post_v2 import signals # pylint: disable=unused-variable
