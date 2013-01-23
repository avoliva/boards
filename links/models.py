from django.db import models
from django.forms import ModelForm, Textarea, TextInput
from django.contrib.auth.models import User


class Category(models.Model):

	# Name of the category
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name


class Link(models.Model):

	# The user who created the link
	user = models.ForeignKey(User, related_name='link_creator')

	# The category the link is placed in
	#@todo: multiple categories for one link
	category = models.ForeignKey(Category)

	# Name/title of the link
	name = models.CharField(max_length=80)

	# Description of the link
	description = models.CharField(max_length=10000)

	# Date the link was created. Automatically set to current time.
	pub_date = models.DateTimeField('date published', auto_now=True, 
		editable=False)

	# Average of votes for the link. Sum of vote rank / vote count
	votes = models.DecimalField(max_digits=5, decimal_places=2, 
		default='0.00', editable=False)

	# Number of votes for the link
	votes_count = models.IntegerField(default=0, editable=False)

	# The link itself. Can be blank
	url = models.URLField(max_length=255, verify_exists=False, 
		null=True, blank=True)

	# The rank of the link. Sum of all votes
	rank = models.IntegerField(default=0, editable=False)

	class Meta:
		# order by descend. newest links first.
		ordering = ['-pub_date']

	def __unicode__(self):
		return self.name


class Profile(models.Model):

	# self explanatory
	user = models.OneToOneField(User)

	# Tokens giving for contributing high quality links
	contrib_tokens = models.IntegerField(default=0, editable=False)

	# People can give you good tokens or bad tokens for whatever reason
	good_tokens = models.IntegerField(default=0, editable=False)
	bad_tokens = models.IntegerField(default=0, editable=False)

	# A quote the user likes
	quote = models.CharField(max_length=1000, null=True, blank=True)

	# @todo
	#avatar = 

	# @todo
	#signature = model.CharField(max_length=)

	def __unicode__(self):
		return self.user.username


class Message(models.Model):

	user = models.ForeignKey(User, related_name='message_creator')

	link = models.ForeignKey(Link, related_name='topic')

	pub_date = models.DateTimeField(auto_now=True, editable=False)

	content = models.CharField(max_length=10000)

	# @todo
	# last_edited = models.DateTimeField(editable=False)
    
    # @todo
	# An array data type for previous edited messages ???

	class Meta:
		ordering = ['pub_date']


class Favorite(models.Model):

	user = models.ForeignKey(User)

	link = models.ForeignKey(Link)


class Vote(models.Model):

	# User who voted for the link
	voter = models.ForeignKey(User)

	# Which link the user voted for
	link = models.ForeignKey(Link)

	vote = models.IntegerField(default=0, editable=False)


# Create form for the link. Uses django form models.
class LinkCreateForm(ModelForm):

	class Meta:
		model = Link
		fields = ('category', 'name', 'description', 'url',)
		widgets = {
            'name': TextInput(attrs={'size': 80}),
            'url': TextInput(attrs={'size': 60}),
            'description': Textarea(attrs={'cols': 100, 'rows': 20}),
        }


class MessageCreateForm(ModelForm):

	class Meta:
		model = Message
		fields = ('content',)
		widgets = {
			'content': Textarea(attrs={'cols': 100, 'rows': 20}),
		}