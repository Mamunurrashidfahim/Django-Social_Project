from django.db.models import fields
from django.forms.widgets import Widget
from App_Login.models import UserProfile
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django.contrib.auth.models import User


class CreateNewUser(UserCreationForm):
    email = forms.EmailField(required=True,label="", widget=forms.EmailInput(attrs={'placeholder':'Enter your Email ','class':'m-3'}))
    first_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Enter your first name','class':'m-3'}))
    last_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Enter your last name','class':'m-3'}))
    username = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Username','class':'m-3'}))
    password1 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'m-3'}))
    password2 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder':'Password confirmation','class':'m-3'}))
    class Meta:
        model = User
        fields = ('first_name','last_name','email','username','password1','password2')

class LoginUser(AuthenticationForm):
    username = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'username','class':'mt-3'}))
    password = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'mt-3'}))
    class Meta:
        model = User
        fields =('username','password')


class EditProfile(forms.ModelForm):
    dob =forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    website =forms.URLField(widget=forms.URLInput(attrs={'value':'http://'}))
    
    class Meta:
        model = UserProfile()
        exclude =('user',)

class ProfileChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')