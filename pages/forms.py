from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Userprofile, Stock, Chickrequest, Farmer, Feedstock,ChickType

# -----------------------------
# User Registration
# -----------------------------
class SignupForm(UserCreationForm):
    class Meta:
        model = Userprofile
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

# -----------------------------
# Stock Management
# -----------------------------
class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = [
            'stock_name', 'quantity', 'chick_type', 'chick_breed',
            'chick_price', 'register_name', 'chick_age'
        ]
        widgets = {
            'stock_name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'chick_type': forms.Select(attrs={'class': 'form-select'}),
            'chick_breed': forms.Select(attrs={'class': 'form-select'}),
            'chick_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'register_name': forms.TextInput(attrs={'class': 'form-control'}),
            'chick_age': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ChickrequestForm(forms.ModelForm):
    class Meta:
        model = Chickrequest
        fields = ['farmer_name', 'chick_type', 'chick_quantity', 'feed_needed', 'chickperiod']
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

        # Set queryset for chick_type dropdown
        self.fields['chick_type'].queryset = ChickType.objects.all()
        # Explicitly set choices for feed_needed
        self.fields['feed_needed'].choices = [('yes', 'Yes'), ('no', 'No')]

        # If farmer is passed, hide field and prefill
        if self.farmer:
            self.fields['farmer_name'].widget = forms.HiddenInput()
            self.initial['farmer_name'] = self.farmer.id

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get("chick_quantity")
        if self.farmer:
            farmer_type = getattr(self.farmer, 'farmer_type', None)
            if farmer_type == 'Starter' and quantity != 100:
                self.add_error('chick_quantity', 'Starter farmers must request exactly 100 chicks.')
            elif farmer_type == 'Returner' and not (1 <= quantity <= 500):
                self.add_error('chick_quantity', 'Returner farmers must request between 1 and 500 chicks.')

# -----------------------------
# Farmer Registration
# -----------------------------
class FarmerRegistrationForm(forms.ModelForm):
    farmer_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Farmer Name')

    class Meta:
        model = Farmer
        fields = [
            'farmer_name', 'farmer_age', 'farmer_gender',
            'farmer_nin', 'farmer_phone_number', 'farmer_type',
            'recomender_name', 'recommender_nin'
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

# -----------------------------
# Feed Stock Management
# -----------------------------
class FeedstockForm(forms.ModelForm):
    class Meta:
        model = Feedstock
        fields = [
            'feed_name', 'feed_quantity', 'cost_price',
            'chick_type', 'feed_type', 'feed_brand', 'feed_supplier',
            'selling_price'
        ]
        widgets = {
            'feed_quantity': forms.NumberInput(attrs={'min': 0}),
            'cost_price': forms.NumberInput(attrs={'min': 0}),
            'selling_price': forms.NumberInput(attrs={'min': 0}),
            'feed_name': forms.TextInput(attrs={'class': 'form-control'}),
            'feed_type': forms.Select(attrs={'class': 'form-control'}),
            'feed_brand': forms.Select(attrs={'class': 'form-control'}),
            'feed_supplier': forms.TextInput(attrs={'class': 'form-control'}),
            'chick_type': forms.Select(attrs={'class': 'form-select'}),
        }
