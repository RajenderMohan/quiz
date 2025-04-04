from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(max_length=100, required=False)
    phone = forms.CharField(max_length=15, required=False)
    age = forms.IntegerField(required=False)
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, required=False)
    dob = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    email = forms.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = ['full_name', 'phone', 'age', 'gender', 'dob', 'email']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=UserProfile.GENDER_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile