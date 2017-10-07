from django import forms

class LoanForm(forms.Form):
    # The other side of the loan
    party = forms.EmailField()

    amount = forms.DecimalField()
    
    # Duration in months
    duration = forms.IntegerField()

    # In decimal format, 1.01 for 1% interest, etc
    interest_rate = forms.DecimalField()
