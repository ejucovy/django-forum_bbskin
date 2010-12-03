from django import forms
from forum.models import Post

class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('thread', 'author', 'time')

    body = forms.CharField(label="Body",
                           widget=forms.Textarea(attrs={'rows':8, 'cols':50}))
