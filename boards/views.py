from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from boards.models import Links, LinksCreateForm, Category, Vote, Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login



class LinksListView(ListView):
	model = Links

	def get_context_data(self, **kwargs):
		c = super(LinksListView, self).get_context_data(**kwargs)
		user = self.request.user
		return c


class LinksDetailView(DetailView):
	model = Links

	def get_context_data(self, **kwargs):

		from decimal import Decimal
		c = super(LinksDetailView, self).get_context_data(**kwargs)
		# Grab the current user.
		user = self.request.user

		# Check for query paramter
		if self.request.GET.get('votes') is not None:

			# Get query parameter
			param = self.request.GET.get('votes')

			# Get link object
			link = c['object']
			try:
				# Check if user voted for link already.
				check = Vote.objects.get(voter=user, link=link)

				# Fixes the ranking for the changed vote
				link.rank = (link.rank - check.vote) + int(param)
				check.vote = int(param)
				check.save()
				
			except Exception as e:
				# Creates a new vote object
				Vote.objects.create(voter=user, link=link, vote=int(param))
				
				# Updates the link object
				link.votes_count += 1
				link.rank += int(param)

			# Saves all changes to the link object
			link.save()

			# Get the links vote average.
			link.votes =  link.rank / Decimal(link.votes_count)
			link.save()

		return c



class LinksCreateView(FormView):

	# Link to the template
	template_name = 'boards/link_create.html'

	# The model that this form uses
	form_class = LinksCreateForm

	def get_context_data(self, **kwargs):
		c = super(LinksCreateView, self).get_context_data(**kwargs)
		user = self.request.user
		return c

	def form_valid(self, form):
		
		# Grabs the form data 
		name = form.cleaned_data['name']
		description = form.cleaned_data['description']
		url = form.cleaned_data['url']
		category = Category.objects.get(id=form.cleaned_data['category'].id)

		# Grabs the current user
		user = self.request.user

		# Creates and saves the link
		link = Links.objects.create(name=name, description=description,
			user=user, category=category, url=url)

		# Redirect URL on success
		self.success_url = '/boards/' + str(link.id)

		return super(LinksCreateView, self).form_valid(form)


class UserListView(ListView):

	def get_context_data(self, **kwargs):
		c = super(UserListView, self).get_context_data(**kwargs)
		user = self.request.user
		return c


# http://blog.bripkens.de/2011/04/adding-custom-profiles-to-the-django-user-model/
class ProfileDetailView(DetailView):
	model = Profile

	def get_context_data(self, **kwargs):
		c = super(ProfileDetailView, self).get_context_data(**kwargs)
		user = self.request.user
		return c