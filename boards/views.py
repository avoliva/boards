from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from boards.models import Links, LinksCreateForm, Category, Vote
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

				link.rank = (link.rank - check.vote) + int(param)
				check.vote = int(param)
				check.save()
				
			except Exception as e:
				Vote.objects.create(voter=user, link=link, vote=int(param))
				link.votes_count += 1
				link.rank += int(param)

			link.save()

			# Get the links vote average.
			link.votes =  link.rank / Decimal(link.votes_count)
			link.save()

		return c



class LinksCreateView(FormView):
	template_name = 'boards/link_create.html'
	form_class = LinksCreateForm

	def form_valid(self, form):
		name = form.cleaned_data['name']
		description = form.cleaned_data['description']
		url = form.cleaned_data['url']
		user = self.request.user
		category = Category.objects.get(id=form.cleaned_data['category'].id)
		link = Links(name=name, description=description, user=user, category=category, url=url)
		link.save()
		self.success_url = '/boards/'

		return super(LinksCreateView, self).form_valid(form)


# class LoginView(FormView):
# 	template_name = 'boards/login.html'
# 	form_class = LoginForm

# 	def form_valid(self, form):
# 		print ("Got Here")
# 		# username = form.cleaned_data['username']
# 		# password = form.cleaned_data['password']
# 		username = self.request.POST['username']
# 		password = self.request.POST['password']
# 		user = authenticate(username=username, password=password)
# 		if user is not None:
# 			# the password verified for the user
# 			if user.is_active:
# 				login(self.request, user)
# 				print("User is valid, active and authenticated")
# 			else:
# 				print("The password is valid, but the account has been disabled!")
# 		else:
# 			# the authentication system was unable to verify the username and password
# 			print("The username and password were incorrect.")

# 		self.success_url = '/boards/'

# 		return super(LoginView, self).form_valid(form)

