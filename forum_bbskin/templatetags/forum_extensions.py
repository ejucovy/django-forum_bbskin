from django import template

from djangohelpers.templatetags import TemplateTagNode

from forum_bbskin.lib import first_post, get_subscription

class GetFirstPost(TemplateTagNode):

    noun_for = {"in":"thread"}

    def __init__(self, varname, thread):
        TemplateTagNode.__init__(self, varname, thread=thread)

    def execute_query(self, thread):
        return first_post(thread)

register = template.Library()
register.tag('get_first_post', GetFirstPost.process_tag)

class GetSubscription(TemplateTagNode):

    noun_for = {"in":"thread", "for":"user"}

    def __init__(self, varname, thread, user):
        TemplateTagNode.__init__(self, varname, thread=thread, user=user)

    def execute_query(self, thread, user):
        return get_subscription(thread, user)

register.tag('get_subscription', GetSubscription.process_tag)

from forum_bbskin.models import Category

class GetCategories(TemplateTagNode):
    noun_for = {}

    def __init__(self, varname):
        TemplateTagNode.__init__(self, varname)

    def execute_query(self):
        return Category.objects.all()

register.tag('get_forum_categories', GetCategories.process_tag)

from forum.models import Thread

class LatestThreads(TemplateTagNode):
    noun_for = {"limit": "limit"}

    def __init__(self, varname, limit):
        TemplateTagNode.__init__(self, varname, limit=limit)

    def execute_query(self, limit):
        limit = int(limit)
        return Thread.objects.order_by('-latest_post_time')[:limit]

register.tag('get_recent_threads', LatestThreads.process_tag)

def pagewise(num, num_pages):
    if num_pages == "first":
        num_pages = 0

    return 10*(int(num_pages) - 1) + int(num)
register.filter('pagewise', pagewise)
