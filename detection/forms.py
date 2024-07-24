from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# User registration form
class CreateUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
	# Checks if the provided email exists
	def clean_email(self):
		if User.objects.filter(email=self.cleaned_data['email']).exists():
			raise forms.ValidationError("El correo proporcionado ya se encuentra registrado.")
		return self.cleaned_data['email']