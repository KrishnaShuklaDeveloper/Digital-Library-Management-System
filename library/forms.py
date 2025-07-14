from django import forms
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta
from .models import Member

### ---- USER SIGNUP FORM ---- ###
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm Password'
    }))
    membership_type = forms.ChoiceField(choices=[('Regular', 'Regular'), ('Premium', 'Premium')],
        widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Member.objects.create(user=user, membership_type=self.cleaned_data['membership_type'])
        return user

### ---- ADMIN MEMBER CREATION FORM ---- ###
class MemberForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter Password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Member.objects.create(user=user)
        return user

### ---- USER PROFILE UPDATE FORM (with image support) ---- ###
class UpdateProfileForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter Email'
    }))
    profile_pic = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Member
        fields = ['profile_pic', 'membership_type']

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['membership_type'].widget.attrs.update({'class': 'form-select'})

### ---- ISSUE BOOK FORM ---- ###
def get_default_due_date():
    return now().date() + timedelta(days=15)

class IssueBookForm(forms.Form):
    member = forms.ModelChoiceField(
        queryset=Member.objects.all(),
        label="Select Member",
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Choose the member who will borrow this book."
    )
    issue_date = forms.DateField(
        label="Issue Date",
        initial=now().date,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        help_text="Date when the book is issued. Defaults to today."
    )
    due_date = forms.DateField(
        label="Due Date",
        initial=get_default_due_date,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        help_text="Date when the book should be returned. Defaults to 15 days from issue."
    )

    def clean(self):
        cleaned_data = super().clean()
        issue_date = cleaned_data.get("issue_date") or now().date()
        due_date = cleaned_data.get("due_date") or (issue_date + timedelta(days=15))

        if due_date <= issue_date:
            raise forms.ValidationError("Due date must be after the issue date.")

        cleaned_data['issue_date'] = issue_date
        cleaned_data['due_date'] = due_date
        return cleaned_data
