from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       
                       url(r'^category-(?P<pk>[0-9]+)/$', 
                           'forum_bbskin.views.forums_in_category',
                           name="forums-in-category"),
                       
                       url(r'^thread/(?P<thread>[0-9]+)/subscription/$', 
                           'forum_bbskin.views.subscribe',
                           name='forum_subscribe_thread'),

                       url(r'^(?P<slug>[-\w]+)/subscription/$', 
                           'forum_bbskin.views.bulk_subscribe',
                           name='forum_subscribe_bulk'),

                       url(r'^edit-post/(?P<pk>[0-9]+)/$',
                           'forum_bbskin.views.edit_post',
                           name='forum-edit-post'),

                       (r'', include('forum.urls')),

)
