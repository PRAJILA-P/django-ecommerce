from django import forms
from .models import Review

class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label="Address")
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="City")
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="State")
    postal_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Postal Code")
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), initial="India", label="Country")

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review...'}),
        }