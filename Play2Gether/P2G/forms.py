from django import forms
from P2G.models import Category, Game


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=64, help_text="Please enter the category name.")
    description = forms.CharField(max_length=4096, help_text="Please give a brief description.",
                                  widget=forms.Textarea(attrs={'cols': 40, 'rows': 10}))
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Category
        fields = ('name', 'description', )


class GameForm(forms.ModelForm):
    name = forms.CharField(max_length=64, help_text="Please enter the Name of the Game")
    link = forms.URLField(max_length=200, help_text="Please enter the URL of the page")
    play_count = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    description = forms.CharField(max_length=4096, help_text="Please give a brief description.",
                                  widget=forms.Textarea(attrs={'cols': 40, 'rows': 10}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), help_text= 'Category')

    class Meta:
        model = Game
        fields = ('name', 'category', 'link', 'description', )
