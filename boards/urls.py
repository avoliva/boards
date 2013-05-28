from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division
from django.conf.urls import patterns, include, url
from boards import views
from boards import models
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import admin
# from . import api
admin.autodiscover()


urlpatterns = patterns(
    '',
    #google stuff
    # url(r'^robots.txt$', views.RobotsTextView.as_view()),
    # url(r'^sitemap.xml$', views.SitemapView.as_view()),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # user functions
    url(r'^login[/]', 'django.contrib.auth.views.login', {'template_name': 'index.html'}, name='login'),
    url(r'^register[/]', views.UserCreateForm.as_view(), name='register'),
    url(r'^logout[/]', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    # boards
    url(r'^$', login_required(views.TopicListView.as_view()), name='topic_list'),
    url(r'^topic/(?P<pk>\d+)[/]', login_required(views.TopicDetailView.as_view()), name='topic'),
    url(r'^tcreate[/]', login_required(views.TopicCreateView.as_view()), name='topic_create'),
    url(r'^mcreate/', views.MessageCreateView.as_view(), name='message_create'),

    # profile options
    url(r'^user/(?P<pk>\d+)[/]$', views.ProfileView.as_view(), name='user_profile'),
    url(r'^user[/]$', views.UserListView.as_view(), name='user_list'),
    url(r'^edit_pass/', views.PasswordResetView.as_view(), name='edit_pass'),
    url(r'^history/', views.TopicHistoryView.as_view(), name='history'),

    #links
    url(r'^links[/]$', login_required(views.LinkListView.as_view(
        queryset=models.Link.objects.filter(
            created__gte=datetime.datetime.now() - datetime.timedelta(days=28)))),
        name='links'),
    url(r'^links/(?P<pk>\d+)[/]$', login_required(views.LinkDetailView.as_view()), name='link'),
    url(r'^lmcreate/', login_required(views.LinkMessageCreateView.as_view()), name='create_link_message'),
    url(r'^lcreate[/]$', login_required(views.LinkCreateView.as_view()), name='link_create'),

    url(r'^links/top[/]$', login_required(views.LinkListView.as_view(
        queryset=models.Link.objects.order_by('-rank'))), name='top_links'),

    url(r'^links/title[/]$', login_required(views.LinkListView.as_view(
        queryset=models.Link.objects.order_by('title'))), name='sort_title'),

    url(r'^links/author[/]$', login_required(views.LinkListView.as_view(
        queryset=models.Link.objects.order_by('user__username'))), name='sort_author'),

    url(r'^links/date[/]$', login_required(views.LinkListView.as_view(
        queryset=models.Link.objects.order_by('created'))), name='sort_date'),

    url(r'^links/rank[/]$', login_required(views.LinkListView.as_view(
        queryset=models.Link.objects.order_by('votes'))), name='sort_rating'),

    # Top rated links of the week
    url(r'^links/top_week[/]$', login_required(views.LinkListView.as_view(
        queryset=models.Link.objects.filter(
            created__gte=datetime.datetime.now()-datetime.timedelta(days=7)).order_by('-rank'))),
        name='top_week'),

    # All links
    url(r'^links/all[/]$', login_required(views.LinkListView.as_view()), name='all_links'),

)


# Static files URL patterns
urlpatterns += staticfiles_urlpatterns()
