from django.apps import AppConfig


class HmBlogConfig(AppConfig):
    name = 'hm_blog'
    def ready(self):
        import hm_blog.signals
