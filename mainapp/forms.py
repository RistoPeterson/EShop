from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class ShippingAddressForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'floatingInput',
        'placeholder': 'Street name and house number',
    }))

    apartment_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'floatingApartment',
        'placeholder': 'Apartment',
    }))

    country = CountryField(blank_label='Select Country').formfield(widget=CountrySelectWidget(attrs={
        'class': 'form-control',
        'id': 'floatingSelect',
        'placeholder': 'Select Country',
        'aria-label': 'Select country',
    }))

    zip_code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'floatingZip',
        'placeholder': 'Zip Code',
    }))
