from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PostModel, ProfileModel, CommentModel
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form_register form-control bg-dark text-white', 
        'placeholder': 'First Name',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form_register form-control bg-dark text-white', 
        'placeholder': 'Username',
        }))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={
        'class': 'form_register form-control bg-dark text-white', 
        'placeholder': 'email'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form_register form-control bg-dark text-white',
        'placeholder': 'password1',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form_register form-control bg-dark text-white',
        'placeholder': 'password1',
    }))

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form_register form-control bg-dark text-white', 
        'placeholder': 'Title',
    }))
    content = RichTextField()
    class Meta:
        model = PostModel
        fields = ['title', 'content']

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form_register form-control bg-dark text-white',
        'placeholder': 'username',
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form_register form-control bg-dark text-white',
        'placeholder': 'password1',
    }))
    bio = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form_register form-control bg-dark text-white',
        'placeholder': 'quote',
    }))
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'bio']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email']:
            self.fields[fieldname].help_text = None

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['user_image']

class PostUpdateForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form_register form-control bg-dark text-white', 
        'placeholder': 'Title',
    }))
    content = RichTextField()
    class Meta:
        model = PostModel
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    content = RichTextField()
    class Meta:
        model = CommentModel
        fields = ['content']