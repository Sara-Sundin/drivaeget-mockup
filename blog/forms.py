from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    A form for submitting comments on blog posts.

    This form is linked to the Comment model and includes only
    the 'body' field. The label is removed to provide a cleaner
    user interface.
    """

    class Meta:
        model = Comment
        fields = ('body',)
        labels = {
            'body': ''  # This removes the "Body" text label
        }