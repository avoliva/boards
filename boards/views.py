from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import UpdateView, TemplateView, FormView, DetailView, ListView
from boards import models
import datetime
from django.contrib.auth import models as auth
from BeautifulSoup import BeautifulSoup


class UserListView(ListView):

    model = auth.User

    template_name = 'user_list.html'

    def get_context_data(self, **kwargs):
        return super(UserListView, self).get_context_data(**kwargs)


class TopicHistoryView(TemplateView):

    model = models.Message

    template_name = 'history.html'

    def get_context_data(self, **kwargs):
        context = super(TopicHistoryView, self).get_context_data(**kwargs)
        context['history'] = models.TopicHistory.objects.filter(user=self.request.user)
        return context


class UserCreateForm(FormView):

    template_name = 'register.html'

    form_class = models.UserCreateForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = auth.User.objects.create_user(username=username, password=password)
        user.save()
        self.success_url = '/'

        return super(UserCreateForm, self).form_valid(form)


class MessageCreateView(FormView):

    template_name = 'message_create.html'

    form_class = models.MessageCreateForm

    def get(self, request, *args, **kwargs):
        if request.GET.get('output') is not None:
            import json
            d = {}
            d['id'] = request.GET.get('id')
            d['topic'] = request.GET.get('topic')
            d['message'] = models.Message.objects.get(pk=d['id']).content
            return HttpResponse(json.dumps(d))
        return super(MessageCreateView, self).get(request)

    def form_valid(self, form):
        if self.request.GET.get('t') is not None:
            try:
                topic = models.Topic.objects.get(pk=self.request.GET.get('t'))
            except ObjectDoesNotExist:
                return HttpResponse("Topic doensn't exist. <a href='/'>Go Home</a>")
            content = form.cleaned_data['content']
            user = self.request.user
            m = models.Message.objects.create(user=user, topic=topic, content=content)
            m.save()
            topic.updated = datetime.datetime.now()
            topic.save()
            try:
                models.TopicHistory.objects.create(user=user, topic=topic, message=m)
            except:
                from django.db import connection
                connection._rollback()
                h = models.TopicHistory.objects.filter(user=user, topic=topic)[0]
                h.message = m
                h.save()
            self.success_url = '/topic/{0}'.format(topic.id)
        return super(MessageCreateView, self).form_valid(form)


class RobotsTextView(TemplateView):
    """
    A simple view with mimetype text/plain
    """
    template_name = 'robots.txt'

    def render_to_response(self, context, **kwargs):
        return super(RobotsTextView, self).render_to_response(
            context,
            content_type='text/plain',
            **kwargs
        )


class SitemapView(TemplateView):
    """
    A simple view with mimetype text/plain
    """
    template_name = 'sitemap.xml'

    def render_to_response(self, context, **kwargs):
        return super(SitemapView, self).render_to_response(
            context,
            content_type='application/xml',
            **kwargs
        )


class TopicListView(ListView):

    model = models.Topic

    template_name = 'topic_list.html'

    def get_context_data(self, **kwargs):
        return super(TopicListView, self).get_context_data(**kwargs)


class TopicDetailView(UpdateView):

    model = models.Topic

    template_name = 'topic_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TopicDetailView, self).get_context_data(**kwargs)
        t = self.object
        messages = models.Message.objects.filter(topic=t)
        if self.request.GET.get('u') is not None:
            messages = models.Message.objects.filter(topic=t, user=self.request.GET.get('u'))
            context['filter'] = "true"
        context['message'] = messages
        return context

    def post(self, request, *args, **kwargs):
        topic = models.Topic.objects.get(pk=request.POST.get('topic'))
        content = request.POST.get('message')
        user = self.request.user
        # soup = BeautifulSoup(content)
        # if soup.quote:
        #     import re
        #     content = '<quote msgid="t,1,3599@1">sdfsdf</quote>'
        #     soup = BeautifulSoup(content)
        #     msgid = soup.quote['msgid']
        #     msgid = re.sub(r'\@', ',', msgid)
        #     u = auth.User.objects.get(pk=msgid.split(',')[1])
        #     m = models.Message.objects.get(pk=msgid.split(',')[2])
        #     content = re.sub(r"\<quote ", "<div class=\"quoted-message\" ", content)
        #     content = re.sub(r"\<\/quote>", "</div>", content)
        #     soup = BeautifulSoup(content)
        #     temp = soup.div.string
        #     soup.div.string = ''
        #     content = soup
        #     content = """{0}<div class="message-header">From: <a href="/user/{1}">{2}</a> | Posted: {3}</div>{4}<br /><br /></div>""".format(content, u.id, u.username, m.created, temp)
        m = models.Message.objects.create(user=user, topic=topic, content=content)
        m.save()
        topic.updated = datetime.datetime.now()
        topic.save()
        try:
            models.TopicHistory.objects.create(user=user, topic=topic, message=m)
        except:
            from django.db import connection
            connection._rollback()
            h = models.TopicHistory.objects.get(user=user, topic__id=topic.id)
            h.message = m
            h.save()
        self.success_url = '/topic/{0}'.format(topic.id)
        return HttpResponseRedirect(self.success_url)


class TopicCreateView(FormView):

    template_name = 'topic_create.html'

    form_class = models.TopicCreateForm

    def form_valid(self, form):
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        t = models.Topic.objects.create(title=title, updated=datetime.datetime.now(), user=self.request.user)
        t.save()
        m = models.Message.objects.create(content=content, user=self.request.user, topic=t)
        m.save()
        try:
            models.TopicHistory.objects.create(user=self.request.user, topic=t, message=m)
        except:
            h = models.TopicHistory.objects.filter(user=self.request.user, topic=t)[0]
            h.message = m
            h.save()
        self.success_url = '/topic/{0}'.format(t.id)
        return super(TopicCreateView, self).form_valid(form)


class ProfileView(DetailView):

    template_name = 'user_profile.html'

    model = auth.User

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        u = self.object
        context['profile'] = u
        return context


class PasswordResetView(FormView):

    form_class = models.PasswordReset

    template_name = 'edit_pass.html'

    def get_context_data(self, **kwargs):
        context = super(PasswordResetView, self).get_context_data(**kwargs)
        if self.request.GET.get('e') is not None:
            if self.request.GET.get('e') == '1':
                context['old_pass'] = "true"
            elif self.request.GET.get('e') == '2':
                context['new_pass'] = "true"
            elif self.request.GET.get('e') == '3':
                context['long'] = "true"
        return context

    def form_valid(self, form):
        password = form.cleaned_data['password']
        if not self.request.user.check_password(password):
            return HttpResponseRedirect('/edit_pass/?e=1')
        new_password = form.cleaned_data['new_password']
        confirm_password = form.cleaned_data['confirm_password']
        if new_password != confirm_password:
            return HttpResponseRedirect('/edit_pass/?e=2')
        self.request.user.set_password(new_password)
        self.request.user.save()
        self.success_url = '/user/{0}'.format(self.request.user.id)
        return super(PasswordResetView, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponseRedirect('/edit_pass/?e=3')


class LinkListView(ListView):

    model = models.Link

    template_name = 'link_list.html'

    def get_context_data(self, **kwargs):
        return super(LinkListView, self).get_context_data(**kwargs)


class LinkDetailView(DetailView):

    model = models.Link

    template_name = 'link_detail.html'

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
                check = models.LinkVote.objects.get(voter=user, link=link)

                # Fixes the ranking for the changed vote
                link.rank = (link.rank - check.vote) + int(param)
                check.vote = int(param)
                check.save()

            # @todo Change to explicit exception DoesNotExist
            except:
                # Creates a new vote object
                models.LinkVote.objects.create(voter=user, link=link, vote=int(param))
                # Updates the link object
                link.votes_count += 1
                link.rank += int(param)

            # Saves all changes to the link object
            link.save()

            # Get the links vote average.
            link.votes = link.rank / Decimal(link.votes_count)
            link.save()

        return c


class LinkCreateView(FormView):

    # Link to the template
    template_name = 'link_create.html'

    # The model that this form uses
    form_class = models.LinkCreateForm

    def form_valid(self, form):
        # Grabs the form data
        name = form.cleaned_data['title']
        description = form.cleaned_data['description']
        url = form.cleaned_data['url']
        # category = models.Category.objects.get(id=form.cleaned_data['category'].id)

        # Grabs the current user
        user = self.request.user

        # Creates and saves the link
        link = models.Link.objects.create(
            title=name,
            description=description,
            user=user,
            # category=category,
            url=url
        )

        # Redirect URL on success
        self.success_url = '/links/' + str(link.id)

        return super(LinkCreateView, self).form_valid(form)


class LinkMessageCreateView(FormView):

    template_name = 'links_message_create.html'

    form_class = models.LinkMessageCreateForm