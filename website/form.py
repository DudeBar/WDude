# coding=utf-8

from django import forms
from website.models import Customer, Billing


class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        super(LoginForm, self).clean()
        if not Customer.objects.filter(login=self.cleaned_data['login']).exists():
            raise forms.ValidationError("Le login n'es pas correct")
        else:
            customer = Customer.objects.get(login=self.cleaned_data['login'])
            if customer.password != self.cleaned_data['password']:
                raise forms.ValidationError("Le mot de passe n'est pas correct")
        return self.cleaned_data


class CreateCustomerForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        super(CreateCustomerForm, self).clean()
        if Customer.objects.filter(login=self.cleaned_data['login']).exists():
            raise forms.ValidationError("Ce login n'est pas disponible")
        if self.cleaned_data["password"] != self.cleaned_data["confirm_password"]:
            raise forms.ValidationError("Les deux mots de passes sont differents")
        return self.cleaned_data


class BillingForm(forms.Form):
    login = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)
    data = forms.CharField(widget=forms.Textarea)

    def clean(self):
        super(BillingForm, self).clean()
        if not Billing.objects.filter(login=self.cleaned_data['login']).exists():
            raise forms.ValidationError("ERROR")
        else:
            billing = Billing.objects.get(login=self.cleaned_data['login'])
            if billing.password != self.cleaned_data['password']:
                raise forms.ValidationError("ERROR")
        return self.cleaned_data