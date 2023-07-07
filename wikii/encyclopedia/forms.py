from django import forms

class NewPageForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    content = forms.CharField(label='Content', widget=forms.Textarea)

class SearchForm(forms.Form):
    query = forms.CharField(label='Search Encyclopedia')
