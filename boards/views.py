from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from boards.models import Links, LinksCreateForm, Category
from django.contrib.auth.models import User


def get_user(request):
	current_user = request.get.user
	return current_user


class LinksListView(ListView):
    model = Links
	# board_list = Board.objects.order_by('id')[:5]
	# #topic_count = topic_count.count()
	# template = loader.get_template('boards/board_list.html')
	# context = Context({
	# 	'board_list': board_list,
	# })
	# return HttpResponse(template.render(context))


class LinksDetailView(DetailView):
	model = Links


	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		from decimal import Decimal
		c = super(LinksDetailView, self).get_context_data(**kwargs)
		if self.request.GET.get('votes') is not None:
			v = self.request.GET.get('votes')
			link = c['object']
			link.rank += int(v)
			link.votes_count += 1
			link.save()
			link.votes =  link.rank / Decimal(link.votes_count)
			link.save()
		user = self.request.user
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
