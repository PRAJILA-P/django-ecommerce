from django import forms

class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label="Address")
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="City")
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="State")
    postal_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Postal Code")
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), initial="India", label="Country")

