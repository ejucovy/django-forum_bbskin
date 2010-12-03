django-forum_bbskin
===================

This package provides some extra models, views, templatetags and templates
on top of Ross Poulton's django-forum to make it more like phpBB and other
bulletin board systems.

You must install django-forum manually from

 http://django-forum.googlecode.com/svn/trunk/
 http://code.google.com/p/django-forum/

and you must have 'forum' in your INSTALLED_APPS.

To get started, add 'forum_bbskin' to your INSTALLED_APPS and re-run syncdb.

Note
----

You should add 'forum_bbskin' ABOVE 'forum' in your INSTALLED_APPS.  This will
allow forum_bbskin's templates to override the ones from django-forum.

Then add a line like

 (r'^forum/', include('forum_bbskin.urls'))

to your root URLconf.

If you've already got django-forum installed:

django-forum_bbskin's URLconf includes django-forum's URLconf, so replace

 (r'^forum/', include('forum.urls'))

with

 (r'^forum/', include('forum_bbskin.urls'))

There is also a CSS file, forum.css, which you should put in your /site_media/css
static directory so that the templates can find it.

Features
========

Forum categories
----------------

forum_bbskin.models.Category adds lightweight categorization to your forums.
Each forum can be associated with any number of categories via the admin
interface.

A view called 'forums-in-category' is provided. By default it will be mounted
at a URL like /forum/category-1/

Subscribe to a thread
---------------------

A view called 'forum_subscribe_thread' is provided. Provided you have the right
permissions, you can POST to this view as a user with POST data
 {'action': 'subscribe'} or {'action': 'unsubscribe'}
to subscribe or unsubscribe.

A template snippet is provided. It is designed to be {% included %} into your
templates with a thread object called 'thread'. An example will be more clear:

{% for thread in listed_threads %}
 {% include 'forum/widgets/subscribe.html' %}
{% endfor %}

This will render a simple form for each thread which allows the user to toggle
her subscription to each thread.

Template tags
-------------

{% load forum_extensions %}

{% get_first_post in thread as first_post %}

{% get_subscription in thread for request.user as subscription %}

{% get_forum_categories as categories %}

{% get_recent_threads limit 5 as recent_threads %}

Templates
---------

The templates are designed to be modular; an attempt was made to factor the templates
into functional units, so that individual pieces could be overridden by the integrator
without forking the whole template directory.  Let me know how well I accomplished that.

The big oversight here is that the templates are full HTML pages.  They should instead
expect to be plugged into a site's template blocks.  That wouldn't be too hard to do.
