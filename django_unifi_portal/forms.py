from random import randint
from django import forms
from django.template import Template
from django.forms import Form, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


PASSWORD = "PASSWORD"


class UnifiLoginForm(Form):
    email = forms.EmailField(label="Email Address", required=True)

    template = Template("""
    <div class="row">
    <div class="input-field col s12 required" id="id_email_container">
        <i class="material-icons prefix">email</i><input id="id_email" name="email" type="email" required="">
        <label for="id_email" class="" required>Email Address</label>
    </div>
    </div>
    """)

    buttons = Template("""
        <button class="waves-effect waves-light btn" type="submit">Login</button>
    """)


    title = "Unifi Login"

    def clean(self):
        email = self.cleaned_data.get('email')
        if email is None:
            raise ValidationError("Email is required")
        user = User.objects.filter(email=email).first()
        if user:
            username = user.username
            self.user = authenticate(self.request, username=username, password=PASSWORD)
        else:
            username = email if len(email) < 30 else email[:25] + str(randint(10000, 99999))
            self.user = User.objects.create(email=email, username=username)
            self.user.set_password(PASSWORD)
            self.user.save()
            self.user = authenticate(self.request, username=username, password=PASSWORD)
        return self.cleaned_data

    def get_user(self):
        return self.user