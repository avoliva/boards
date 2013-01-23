from django.conf.urls import patterns, url
from boards.views import LinksListView, LinksDetailView, LinksCreateView
from boards.models import Links
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template

from boards import views

urlpatterns = patterns('',

	# New links, created in the last 28 days.
	url(r'^$', login_required(LinksListView.as_view(
		queryset=Links.objects.filter(
			pub_date__gte=datetime.now()-timedelta(days=28)))), 
		name='links'),

	# Specific link
	url(r'^(?P<pk>\d+)[/]$', login_required(LinksDetailView.as_view()), name='link'),

	# Link Creation
	url(r'^create[/]$', login_required(LinksCreateView.as_view()), name='link_create'),

	# Top rated links of all time
	url(r'^top[/]$', login_required(LinksListView.as_view(
		queryset=Links.objects.order_by("-rank"))),
		name='top_rank'),

	# Top rated links of the week
	url(r'^top_week[/]$', login_required(LinksListView.as_view(
		queryset=Links.objects.filter(
			pub_date__gte=datetime.now()-timedelta(days=7)).order_by('-rank'))),
		name='top_week'),

	# All links
	url(r'^all[/]$', login_required(LinksListView.as_view()), name='all_links'),

	# Login page
	url(r'^login[/]$', 'django.contrib.auth.views.login', 
		{'template_name': 'boards/login.html'}),

	# Logout page
	url(r'^logout[/]$', 'django.contrib.auth.views.logout', 
		{'template_name': 'boards/logout.html',
		 'next_page' : '/boards/login'}),
)
