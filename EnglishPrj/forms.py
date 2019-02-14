from django import forms

class IdForm(forms.Form):
    login = forms.CharField(label='ISU Login', max_length=30)
    # password = forms.CharField(label='Password', max_length=40)
    password = forms.CharField(widget=forms.PasswordInput())

class ProfileForm(forms.Form):
    access = forms.CharField(label='access', max_length=40)
    lastname = forms.CharField(label='lastname', max_length=40)
    name = forms.CharField(label='name', max_length=40)
    middlename = forms.CharField(label='middlename', max_length=40)