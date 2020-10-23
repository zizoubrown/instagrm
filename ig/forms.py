from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

class SignupForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(), max_length=30, required=True,)
	email = forms.CharField(widget=forms.EmailInput(), max_length=100, required=True,)
	password = forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Confirm your password.")

	class Meta:

		model = User
		fields = ('username', 'email', 'password')

	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		self.fields['username'].validators.append(ForbiddenUsers)
		self.fields['username'].validators.append(InvalidUser)
		self.fields['username'].validators.append(UniqueUser)
		self.fields['email'].validators.append(UniqueEmail)

	def clean(self):
		super(SignupForm, self).clean()
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')

		if password != confirm_password:
			self._errors['password'] = self.error_class(['Passwords do not match. Try again'])
		return self.cleaned_data