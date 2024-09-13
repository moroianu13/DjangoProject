from django import forms
from django.contrib.auth.models import User
from .models import Category , Item , Review

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'user', 'category']  # Fields to be shown in the form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)], attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }