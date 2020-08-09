from django import forms 
from django.contrib.auth.models import User
from .models import Comment
from bootstrap_modal_forms.forms import BSModalModelForm

class CommentForm(BSModalModelForm):
    
    class Meta:
        model = Comment
        fields = ("text")
)
