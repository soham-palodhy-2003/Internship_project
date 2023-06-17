from django.shortcuts import render,redirect
from myproject.settings import INTERNAL_RESET_SESSION_TOKEN
from onlineclasses.forms import RegistrationForm,LoginForm
from django.contrib.auth import logout,login
from django.views import View
from django.contrib.auth.models import User

from django.views.generic.edit import FormView


from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model,login as auth_login
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.translation import gettext_lazy as _

class SignupView(FormView):
    template_name = 'courses/signup.html'
    form_class = RegistrationForm
    success_url = '/login'
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'courses/login.html'
    form_class = LoginForm
    success_url = "/"

    def form_valid(self, form):
        print("Form is valid",form.cleaned_data)
        login(self.request,form.cleaned_data)
        return super().form_valid(form)
 
def signout(request):
    logout(request)
    return redirect("home")

user = get_user_model()

class CustomPasswordResetView(PasswordResetView,FormView):
    email_template_name = "registration/password_reset_email.html"
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")
    template_name = "registration/password_reset_form.html"
    title = ("Password reset")
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)

      
class CustomPasswordResetDoneView(PasswordResetDoneView):
   template_name = 'password_reset_sent.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = "set-password"
    success_url = reverse_lazy("password_reset_complete")
    template_name = "registration/password_reset_confirm.html"
    title = ("Enter new password")
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if "uidb64" not in kwargs or "token" not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )

        self.validlink = False
        self.user = self.get_user(kwargs["uidb64"])

        if self.user is not None:
            token = kwargs["token"]
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(
                        token, self.reset_url_token
                    )
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context["validlink"] = True
        else:
            context.update(
                {
                    "form": None,
                    "title": _("Password reset unsuccessful"),
                    "validlink": False,
                }
            )
        return context


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
     template_name = 'password_reset_complete.html'