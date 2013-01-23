from django.conf.urls import patterns, url
from boards.views import LinksListView, LinksDetailView, LinksCreateView
from boards.models import Links
from datetime import datetime, timedelta

from boards import views

urlpatterns = patterns('',

	# New links, created in the last 28 days.
	url(r'^$', LinksListView.as_view(
		queryset=Links.objects.filter(
			pub_date__gte=datetime.now()-timedelta(days=28))), 
		name='links'),

	# Specific link
	url(r'^(?P<pk>\d+)[/]$', LinksDetailView.as_view(), name='link'),

	# Link Creation
	url(r'^create[/]$', LinksCreateView.as_view(), name='link_create'),

	# Top rated links of all time
	url(r'^top[/]$', LinksListView.as_view(
		queryset=Links.objects.order_by("-rank")),
		name='top_rank'),

	# Top rated links of the week
	url(r'^top_week[/]$', LinksListView.as_view(
		queryset=Links.objects.filter(
			pub_date__gte=datetime.now()-timedelta(days=7)).order_by('-rank')),
		name='top_week'),

	# All links
	url(r'^all$', LinksListView.as_view(), name='all_links'),
)
