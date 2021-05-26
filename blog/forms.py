from django import forms
from .models import Post, Comment#, Profile
from django.contrib.auth.forms import UserCreationForm #for custom user creation
from django.contrib.auth.models import User #for custom user creation
from django.core.exceptions import ValidationError #for custom user creation

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'make_public',)
    
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter Email')
    password1 = forms.CharField(label='Enter Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

        
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if len(password1) < 7:
            raise ValidationError("Passwords length needs to be at least 7 characters")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user
class SignUpForm(UserCreationForm):
    #mob = forms.CharField(max_length=10) #Custom field
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
        labels = {
            #'mob':'Mobile Phone',
            'email':'Email Adress Goes Here',
            }#Custom Label
