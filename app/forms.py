from django import forms
from django.contrib.auth.models import User

from app.draw import is_code_valid
from app.models import Draw, UserProfile, Deposit
from django import template

register = template.Library()


@register.filter(name='addClass')
def addClass(field, css_class):
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={"class": css_class})
    return field.label_tag(attrs={"class": css_class})


class DrawForm(forms.ModelForm):
    class Meta:
        model = Draw
        fields = ('code',)
        labels = {
            'code': 'Stake',
        }

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get("code")

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg'}))
    fullname = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))  # Fullname field

    class Meta:
        model = UserProfile
        fields = ['fullname', 'email']  # Only include the fields you want to display

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already taken.")
        return email

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email']
        )
        user.set_password(self.cleaned_data['password'])  # Set hashed password

        if commit:
            user.save()  # Save User instance
            # Create UserProfile instance
            user_profile = UserProfile(user=user, fullname=self.cleaned_data['fullname'])
            user_profile.save()

        return user
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))

class DepositForm(forms.ModelForm):
    options = [
        ('crypto', 'Crypto'),
        ('gift_card', 'Gift Card'),
    ]
    deposit_options = forms.ChoiceField(
        choices=options,
        widget=forms.Select,
        label="Method",
        required=True
    )
    
    class Meta:
        model = Deposit
        fields = ('amount',)  # Ensure this is a tuple with a trailing comma

class WithdrawForm(forms.ModelForm):
    options = [
        ('crypto', 'Crypto'),
        ('paypal', 'PayPal'),
        ('gcash', 'Gcash'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    withdrawal_options = forms.ChoiceField(
        choices=options,
        widget=forms.Select,
        label="Method",
        required=True
    )
    
    class Meta:
        model = Deposit
        fields = ('amount',)  # Ensure this is a tuple with a trailing comma