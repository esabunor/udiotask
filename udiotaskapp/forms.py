from django import forms
from .models import Person


class PersonCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={}))
    email = forms.CharField(widget=forms.TextInput(attrs={}))

    class Meta:
        fields = ['email', 'name']
        model = Person

    def clean_email(self):
        email = self.cleaned_data['email']
        if Person.objects.filter(email=email).exists():
            self.add_error("email", "email already exists")
        return email


class PersonFilterForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={}), required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={}), required=False)
