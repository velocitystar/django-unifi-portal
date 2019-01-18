from random import randint
from django import forms
from django.template import Template
from django.forms import Form
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


PASSWORD = "PASSWORD"


class UnifiLoginForm(Form):
    email = forms.EmailField(label="Email Address", required=True)

    template = Template("""
    {% form %}
        {% part form.email prefix %}<i class="material-icons prefix">email</i>{% endpart %}
    {% endform %}
    """)

    buttons = Template("""
        <button class="waves-effect waves-light btn" type="submit">Login</button>
    """)


    title = "Unifi Login"

    def clean(self):
        email = self.cleaned_data.get('email')
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