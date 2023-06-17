from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=25, required=True,label='username')

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = None

        try:
            user = User.objects.get(username=username)
            result = authenticate(username=user.username, password=password)
            if result is not None:
                return result
            else:
                raise forms.ValidationError("Invalid credentials")
        except User.DoesNotExist:
            raise forms.ValidationError("Invalid Credentials")
