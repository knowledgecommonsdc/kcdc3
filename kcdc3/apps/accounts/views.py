from django import forms
from django.utils.translation import ugettext_lazy as _
from userena.forms import SignupForm
from models import ExtendedProfile

class SignupFormExtra(SignupForm):
	"""
	See http://docs.django-userena.org/en/latest/faq.html#how-do-i-add-extra-fields-to-forms
	"""
	first_name = forms.CharField(label=_(u'What name would you like us to use?'),
								 max_length=50,
								 required=True)

	last_name = forms.CharField(label=_(u'What is your full name?'),
								max_length=100,
								required=True)
	phone_number = forms.CharField(max_length=32, required=False)
	zipcode = forms.CharField(max_length=5, required=False)

	def __init__(self, *args, **kw):
		"""

		A bit of hackery to get the first name and last name at the top of the
		form instead at the end.

		"""
		super(SignupFormExtra, self).__init__(*args, **kw)
		# Put the first and last name at the top
		new_order = self.fields.keyOrder[:-4]
		new_order.insert(0, 'last_name')
		new_order.insert(1, 'first_name')
		new_order.insert(2, 'phone_number')
		new_order.insert(3, 'zipcode')
		self.fields.keyOrder = new_order

	def save(self):
		"""
		Override the save method to save the first and last name to the user
		field.

		"""
		# First save the parent form and get the user.
		new_user = super(SignupFormExtra, self).save()

		new_user.first_name = self.cleaned_data['first_name']
		new_user.last_name = self.cleaned_data['last_name']
		new_user.save()

		# create profile for this user
		user_profile = new_user.get_profile()
		user_profile.phone_number = self.cleaned_data['phone_number']
		user_profile.zipcode = self.cleaned_data['zipcode']
		user_profile.save()

		# Userena expects to get the new user from this form, so return the new
		# user.
		return new_user


