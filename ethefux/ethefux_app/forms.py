from django import forms
from django.core.validators import EmailValidator

class LoanForm(forms.Form):
    # The other side of the loan
    party = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Email of other party', 'autofocus':'1'}),
                            max_length=150, validators=[EmailValidator])

    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Loan Amount'}))
    
    # Duration in months
    duration = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Duration (Months)'}))

    # In decimal format, 1.01 for 1% interest, etc
    interest_rate = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':"Interest Rate (Monthly)"}))

    class Meta:
        fields = ('party', 'amount', 'duration', 'interest_rate')
