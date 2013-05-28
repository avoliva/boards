from django.db import models
from django import forms
from django.contrib.auth import models as auth


class Timestamp(models.Model):
    """Identifies when an inherited model has been created and last updated.
    """

    class Meta:
        abstract = True

    #! Date and time the model was created.
    created = models.DateTimeField(auto_now_add=True, editable=False)

    #! Date and time the model was last updated.
    updated = models.DateTimeField(auto_now=True, editable=False)


class Topic(Timestamp):

    class Meta:
        ordering = ['-updated']

    user = models.ForeignKey(auth.User)

    title = models.CharField(max_length=32765)

    def message_count(self):
        return Message.objects.filter(topic=self).count()

    def __unicode__(self):
        return self.title


class Message(Timestamp):

    class Meta:
        ordering = ['created']

    user = models.ForeignKey(auth.User)

    topic = models.ForeignKey(Topic)

    content = models.CharField(max_length=32765)

    def __unicode__(self):
        return self.content[:20]


class TopicHistory(Timestamp):

    class Meta:
        ordering = ['-topic__updated']
        unique_together = ('user', 'topic',)

    user = models.ForeignKey(auth.User)

    message = models.ForeignKey(Message)

    topic = models.ForeignKey(Topic)


class UserCreateForm(forms.ModelForm):

    class Meta:
        model = auth.User
        fields = ('username', 'password',)
        widgets = {
            'username': forms.TextInput(attrs={'size': 60}),
            'password': forms.PasswordInput(attrs={'size': 60}),
        }


class MessageCreateForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'input-xxlarge', 'rows': 20, 'cols': 100})
        }


class TopicCreateForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(attrs={'size': 60}),
        }

    content = forms.CharField("Message", min_length=3, widget=forms.Textarea(attrs={'rows': 20, 'cols': 100, 'class': 'input-xxlarge'}))


class PasswordReset(forms.ModelForm):

    class Meta:
        model = auth.User
        fields = ('password',)
        widgets = {
            'password': forms.PasswordInput(attrs={'size': 60}),
        }

    new_password = forms.CharField("New Password", min_length=8, widget=forms.PasswordInput(attrs={'size': 60}))

    confirm_password = forms.CharField("New Password", min_length=8, widget=forms.PasswordInput(attrs={'size': 60}))


class Category(Timestamp):

    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Link(Timestamp):

    user = models.ForeignKey(auth.User, related_name='link_creator')

    category = models.ManyToManyField(Category, null=True, blank=True)

    title = models.CharField(max_length=80)

    description = models.CharField(max_length=32765)

    votes = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default='0.00',
        editable=False
    )

    votes_count = models.IntegerField(default=0, editable=False)

    url = models.URLField(
        max_length=255,
        null=True,
        blank=True
    )

    rank = models.IntegerField(default=0, editable=False)

    class Meta:

        ordering = ['-created']

    def __unicode__(self):
        return self.title


class LinkVote(Timestamp):

    # User who voted for the link
    voter = models.ForeignKey(auth.User)

    # Which link the user voted for
    link = models.ForeignKey(Link)

    vote = models.IntegerField(default=0, editable=False)


class LinkFavorite(Timestamp):

    user = models.ForeignKey(auth.User)

    link = models.ForeignKey(Link)

    def __unicode__(self):
        return '{0}:{1}'.format(self.user, self.link)


class LinkMessage(Timestamp):

    class Meta:
        ordering = ['created']

    user = models.ForeignKey(auth.User)

    link = models.ForeignKey(Link)

    content = models.CharField(max_length=32765)

    def __unicode__(self):
        return self.content[:20]


class LinkCreateForm(forms.ModelForm):

    class Meta:
        model = Link
        fields = ('category', 'title', 'description', 'url',)
        widgets = {
            'title': forms.TextInput(attrs={'size': 80}),
            'url': forms.TextInput(attrs={'size': 60}),
            'description': forms.Textarea(attrs={'cols': 100, 'rows': 20}),
        }


class LinkMessageCreateForm(forms.ModelForm):

    class Meta:
        model = LinkMessage
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'cols': 100, 'rows': 20}),
        }
