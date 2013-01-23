from django.db import models
from django.forms import ModelForm, Textarea, TextInput
from django.contrib.auth.models import User


class Category(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name


class Links(models.Model):
	user = models.ForeignKey(User, related_name='link_creator')
	category = models.ForeignKey(Category)
	name = models.CharField(max_length=80)
	description = models.CharField(max_length=10000)
	pub_date = models.DateTimeField('date published', auto_now=True, editable=False)
	votes = models.DecimalField(max_digits=5, decimal_places=2, default='0.00', editable=False)
	votes_count = models.IntegerField(default=0, editable=False)
	url = models.CharField(max_length=255, default='n')
	rank = models.IntegerField(default=0, editable=False)

	class Meta:
		ordering = ['-pub_date']

	def __unicode__(self):
		return self.name

class LinksCreateForm(ModelForm):
	class Meta:
		model = Links
		fields = ('category', 'name', 'description', 'url')
		widgets = {
            'name': TextInput(attrs={'size': 80}),
            'url': TextInput(attrs={'size': 60}),
            'description': Textarea(attrs={'cols': 100, 'rows': 20}),
        }
