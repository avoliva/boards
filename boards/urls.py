from django.conf.urls import patterns, url
from boards.views import LinksListView, LinksDetailView, LinksCreateView

from boards import views

urlpatterns = patterns('',
	url(r'^$', LinksListView.as_view(), name='links'),
	url(r'^(?P<pk>\d+)[/]$', LinksDetailView.as_view(), name='link'),
	url(r'^(?P<pk>\d+)[/]\\?votes=[0-9]?[0-9]$', LinksDetailView.as_view(), name='link'),
	url(r'^create[/]$', LinksCreateView.as_view(), name='link_create'),

)