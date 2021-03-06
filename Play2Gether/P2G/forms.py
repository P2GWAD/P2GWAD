from django import forms
from P2G.models import Category, Game
from django.contrib.auth.models import User
from P2G.models import Category, Game, Group, UserProfile, Score


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=64, help_text="Please enter the category name.")
    description = forms.CharField(max_length=4096, help_text="Please give a brief description.",
                                  widget=forms.Textarea(attrs={'cols': 40, 'rows': 10}))
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Category
        fields = ('name', 'description',)


class GameForm(forms.ModelForm):
    name = forms.CharField(max_length=64, help_text="Please enter the Name of the Game")
    link = forms.URLField(max_length=200, help_text="Please enter the URL of the page")
    play_count = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    description = forms.CharField(max_length=4096, help_text="Please give a brief description.",
                                  widget=forms.Textarea(attrs={'cols': 40, 'rows': 10}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), help_text='Category')

    class Meta:
        model = Game
        fields = ('name', 'category', 'link', 'description',)


class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(max_length=4096, widget=forms.Textarea(attrs={'cols': 40, 'rows': 10}))

    class Meta:
        model = UserProfile
        fields = ('profile_image', 'bio',)


class GroupForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the name of the Group.")
    game = forms.ModelChoiceField(queryset=Game.objects.all(), help_text='Game')
    class Meta:
        model = Group
        fields = ('name', 'game',)
