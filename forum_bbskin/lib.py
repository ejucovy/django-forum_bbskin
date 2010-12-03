from forum.models import Post

def get_subscription(thread, user):
    return thread.subscription_set.select_related().filter(
        author=user)

def first_post(thread):
    return Post.objects.filter(thread__pk=thread.id).order_by('time')[0]
