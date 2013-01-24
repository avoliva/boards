from django.views.generic import ListView, DetailView, FormView
from links.models import Link, LinkCreateForm, Category, Vote, Profile,\
 MessageCreateForm, Message
from django.contrib.auth.models import User


class LinkListView(ListView):
	model = Link

	def get_context_data(self, **kwargs):
		c = super(LinkListView, self).get_context_data(**kwargs)
		user = self.request.user
		return c


class LinkDetailView(DetailView):
	model = Link

	def get_context_data(self, **kwargs):

		from decimal import Decimal
		c = super(LinkDetailView, self).get_context_data(**kwargs)

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
				
			# @todo Change to explicit exception DoesNotExist
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


class LinkCreateView(FormView):

	# Link to the template
	template_name = 'links/link_create.html'

	# The model that this form uses
	form_class = LinkCreateForm

	def form_valid(self, form):
		
		# Grabs the form data 
		name = form.cleaned_data['name']
		description = form.cleaned_data['description']
		url = form.cleaned_data['url']
		category = Category.objects.get(id=form.cleaned_data['category'].id)

		# Grabs the current user
		user = self.request.user

		# Creates and saves the link
		link = Link.objects.create(name=name, description=description,
			user=user, category=category, url=url)

		# Redirect URL on success
		self.success_url = '/links/' + str(link.id)

		return super(LinkCreateView, self).form_valid(form)


class MessageCreateView(FormView):

	template_name = 'links/message_create.html'

	form_class = MessageCreateForm

	def form_valid(self, form):
		if self.request.GET.get('link') is not None:
			param = self.request.GET.get('link')
			user = self.request.user
			content = form.cleaned_data['content']
			try:
				link = Link.objects.get(id=int(param))
				Message.objects.create(user=user, link=link, content=content)
			except Exception as e:
				print "error"
			self.success_url = '/links/' + str(link.id)

			return super(MessageCreateView, self).form_valid(form)


class UserListView(ListView):

	def get_context_data(self, **kwargs):
		c = super(UserListView, self).get_context_data(**kwargs)
		user = self.request.user
		return c


class ProfileDetailView(DetailView):
	model = Profile

	def get_context_data(self, **kwargs):
		c = super(ProfileDetailView, self).get_context_data(**kwargs)
		user = self.request.user
		return c


class MessageDetailView(DetailView):
	model = Message

	def get_context_data(self, **kwargs):
		c = super(MessageDetailView, self).get_context_data(**kwargs)
		user = self.request.user
		return c

class MessageListView(ListView):
	model = Message

	def get_context_data(self, **kwargs):
		c = super(MessageListView, self).get_context_data(**kwargs)
		user = self.request.user
		return c
