from django import forms
from django.contrib.auth.models import User
from rango.models import Category, Game, Group, , UserProfile, Score

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('profile_image', 'bio',)

