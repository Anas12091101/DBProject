from django import forms

class resetforms(forms.Form):
    password = forms.CharField(label='Password',
                        widget = forms.PasswordInput)
    confirm = forms.CharField(label='Confirm',
                        widget = forms.PasswordInput)