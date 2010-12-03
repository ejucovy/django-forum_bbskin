from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404

from djangohelpers.lib import rendered_with

from forum.models import Thread, Subscription, Forum, Post

from forum_bbskin.models import Category

LOGIN_URL = getattr(settings, 'LOGIN_URL', '/accounts/login/')

@rendered_with('forum/forum_category_list.html')
def forums_in_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    return {'category': category}

from forum_bbskin.forms import EditForm
from django.db import models

@rendered_with('forum/edit_post.html')
def edit_post(request, pk):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('%s?next=%s' % (LOGIN_URL, request.path))

    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        if not request.user.is_staff:
            return HttpResponseForbidden()

    if request.method == "POST":
        form = EditForm(request.POST, instance=post)
        if not form.is_valid():
            return {'form': form, 'post': post}
        body = form.cleaned_data['body']
        post.body = body
        models.Model.save(post) # circumvent funny stuff in Post.save
        return HttpResponseRedirect(post.thread.get_absolute_url())
        
    form = EditForm(instance=post)
    return {'form': form, 'post': post}

def subscribe(request, thread):
    
    if request.method != "POST":
        return HttpResponseRedirect('..')

    if not request.user.is_authenticated():
        return HttpResponseRedirect('%s?next=%s' % (LOGIN_URL, request.path))

    t = get_object_or_404(Thread, pk=thread)
    if t.closed:
        return HttpResponseServerError()
    if not Forum.objects.has_access(t.forum, request.user.groups.all()):
        return HttpResponseForbidden()


    sub = Subscription.objects.filter(thread=t, author=request.user)
    action = request.POST.get('action', False)
    if not action:
        return HttpResponseRedirect(t.get_absolute_url())
        
    if action == "Subscribe":
        if not sub:
            s = Subscription(
                author=request.user,
                thread=t
                )
            s.save()
    elif action == "Unsubscribe":
        if sub:
            sub.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER') or 
                                t.get_absolute_url())


def bulk_subscribe(request, slug):

    if request.method != "POST":
        return HttpResponseRedirect('..')

    if not request.user.is_authenticated():
        return HttpResponseRedirect('%s?next=%s' % (LOGIN_URL, request.path))

    try:
        forum = Forum.objects.for_groups(
            request.user.groups.all()).select_related().get(slug=slug)
    except Forum.DoesNotExist:
        raise Http404

    available_threads = forum.thread_set.filter(closed=False)
    
    action = request.POST.get('action', False)
    if not action:
        return HttpResponseRedirect(forum.get_absolute_url())
    
    if action == "Subscribe":
        for thread in available_threads:
            s, created = Subscription.objects.get_or_create(
                author=request.user,
                thread=thread)
            if created:
                s.save()
    elif action == "Unsubscribe":
        subs = Subscription.objects.filter(thread__forum=forum, 
                                           author=request.user)
        subs.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER') or 
                                forum.get_absolute_url())
