#!/usr/bin/env python
# coding: utf-8

import time
from django.http import HttpResponseForbidden
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.http import is_safe_url
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.conf import settings

from .unifi_client import UnifiClient
from django_unifi_portal import forms
from django_unifi_portal.models import UnifiUser

class UserAuthorizeView(TemplateView):
    """ Authorize a guest based on parameters passed through the request. """
    template_name = 'index.html'

    def get_user_profile_inst(self):
        return UnifiUser.objects.get_or_create(user=self.request.user)[0]

    def get_context_data(self, **kwargs):
        """Update view context."""
        context = super(UserAuthorizeView, self).get_context_data(**kwargs)

        _mac = self.request.GET.get('id', '')
        _ap = self.request.GET.get('ap', '')
        _url = self.request.GET.get('url', '')
        _t = settings.UNIFI_TIMEOUT_MINUTES
        _last_login = time.strftime("%c")

        context.update({
            'guest_mac': _mac,
            'ap_mac': _ap,
            'minutes': _t,
            'url': _url,
            'last_login': _last_login
        })
        print("context->", context)

        # Saving info on userprofile Model
        userprofile = self.get_user_profile_inst()
        if userprofile:
            userprofile.guest_mac = _mac
            userprofile.last_backend_login = _last_login
            userprofile.save()

        # Ask authorization to unifi server
        unifi_client = UnifiClient()
        status_code = unifi_client.send_authorization(_mac, _ap, _t)
        if status_code != 200:
            context['Unauthorized'] = True
        time.sleep(3)
        return context

    def post(self, request, *args, **kwargs):
        """Deny post requests."""
        return HttpResponseForbidden()

    def get(self, request, *args, **kwargs):
        """Response with rendered html template."""
        context = self.get_context_data()

        if 'Unauthorized' in context:
            self.template_name = 'forbidden.html'
            return self.render_to_response(context)

        return self.render_to_response(context)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserAuthorizeView, self).dispatch(request, *args, **kwargs)


class UnifiUserLogin(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    template_name = 'login.html'
    success_url = reverse_lazy('index')
    form_class = forms.UnifiLoginForm
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_form(self, form_class=None):
        print('get_form?')
        form = super(UnifiUserLogin, self).get_form(form_class)
        form.request = self.request
        return form

    @method_decorator(csrf_exempt)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        # Set the request url from unifi into a cookie to get in registration form
        try:
            request.session['mynext'] = self.request.GET['next']
        except Exception as e:
            print("EXCEPTION:UnifiUserLogin " + str(e))
            pass

        return super(UnifiUserLogin, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(UnifiUserLogin, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to
