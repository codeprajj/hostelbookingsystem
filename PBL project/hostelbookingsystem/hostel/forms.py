from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email (optional)'})
    )
    gender = forms.ChoiceField(
        choices=UserProfile.GENDER_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'gender', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if self.cleaned_data.get('email'):
            user.email = self.cleaned_data['email']
        
        gender = self.cleaned_data['gender']  # Store gender before saving user
        
        if commit:
            # Save user first
            user.save()
            
            # Create or get profile and set gender IMMEDIATELY
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.gender = gender
            profile.save(update_fields=['gender'])  # Only update gender field
            
            # Force refresh and verify
            profile.refresh_from_db()
            if profile.gender != gender:
                # If still wrong, try one more time
                UserProfile.objects.filter(user=user).update(gender=gender)
                profile.refresh_from_db()
        
        return user
