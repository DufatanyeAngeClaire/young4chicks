from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Userprofile, Chickrequest
from .models import Farmer

class SignupForm(UserCreationForm):
    class Meta:
        model = Userprofile
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

class ChickrequestForm(forms.ModelForm):
    class Meta:
        model = Chickrequest
        fields = [
            'farmer_name',
            'chick_type',
            'chick_quantity',
            'feed_needed',
            'chickperiod',
        ]
        widgets = {
            'farmer_name': forms.Select(attrs={'class': 'form-control'}),
            'chick_type': forms.Select(attrs={'class': 'form-control'}),
            'chick_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'feed_needed': forms.Select(attrs={'class': 'form-control'}),
            'chickperiod': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.farmer = kwargs.pop('farmer', None)
        super().__init__(*args, **kwargs)

        # Auto-hide farmer_name if farmer provided
        if self.farmer:
            self.fields['farmer_name'].widget = forms.HiddenInput()
            self.initial['farmer_name'] = self.farmer.id

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get("chick_quantity")

        if self.farmer:
            farmer_type = getattr(self.farmer, 'farmer_type', None)

            if farmer_type == 'starter' and quantity != 100:
                self.add_error('chick_quantity', 'Starter farmers must request exactly 100 chicks.')

            elif farmer_type == 'returning' and (quantity < 1 or quantity > 500):
                self.add_error('chick_quantity', 'Returning farmers must request between 1 and 500 chicks.')


class FarmerRegistrationForm(forms.ModelForm):
    farmer_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Farmer Name'
    )

    class Meta:
        model = Farmer
        fields = [
            'farmer_name',
            'farmer_age',
            'farmer_gender',
            'farmer_nin',
            'farmer_phone_number',
            'farmer_type',
            'recomender_name',
            'recommender_nin',
        ]
        widgets = {
            'farmer_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'farmer_gender': forms.Select(attrs={'class': 'form-control'}),
            'farmer_nin': forms.TextInput(attrs={'class': 'form-control'}),
            'farmer_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'farmer_type': forms.Select(attrs={'class': 'form-control'}),
            'recomender_name': forms.TextInput(attrs={'class': 'form-control'}),
            'recommender_nin': forms.TextInput(attrs={'class': 'form-control'}),
        }

