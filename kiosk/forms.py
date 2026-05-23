from django import forms
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class AgeVerificationForm(forms.Form):
    customer_name = forms.CharField(
        max_length=100,
        required=True,
        label="Full Name",
        widget=forms.TextInput(attrs={
            'class': 'form-input form-input-half',
            'placeholder': 'Enter your full name',
            'autocomplete': 'name'
        })
    )
    
    customer_contact = forms.CharField(
        max_length=100,
        required=False,
        label="Phone Number or Email (Optional)",
        widget=forms.TextInput(attrs={
            'class': 'form-input form-input-half',
            'placeholder': 'Phone number or Email',
            'autocomplete': 'tel'
        })
    )
    
    birthdate = forms.DateField(
        required=True,
        label="Date of Birth",
        widget=forms.DateInput(attrs={
            'class': 'form-input',
            'type': 'date',
            'min': '1950-01-01',
            'max': '2010-12-31'
        }),
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m-%d-%Y']
    )
    
    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate:
            # Check if birthdate is within acceptable range (1950-2010)
            min_date = date(1950, 1, 1)
            max_date = date(2010, 12, 31)
            
            if birthdate < min_date:
                raise forms.ValidationError(
                    "Please enter a birth date after January 1, 1950."
                )
            
            if birthdate > max_date:
                raise forms.ValidationError(
                    "Please enter a birth date before December 31, 2010."
                )
            
            # Calculate age
            today = date.today()
            age = relativedelta(today, birthdate).years
            
            # Check if user is at least 21 years old
            if age < 21:
                raise forms.ValidationError(
                    f"You must be at least 21 years old to access our products. "
                    f"You are currently {age} years old."
                )
                
            # Check if birthdate is not in the future
            if birthdate > today:
                raise forms.ValidationError("Date of birth cannot be in the future.")
        
        return birthdate
    
    def get_age(self):
        """Calculate and return the user's age"""
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate:
            today = date.today()
            return relativedelta(today, birthdate).years
        return None
