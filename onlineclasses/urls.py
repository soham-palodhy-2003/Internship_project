from django.urls import path
from onlineclasses.views import home,verifypayment,my_courses
from onlineclasses.views.courses import course_page
from onlineclasses.views.contact_us import contact_us
from onlineclasses.views.explore_courses import explore_courses
from onlineclasses.views import SignupView,LoginView,signout,checkout
from onlineclasses.views.auth import(
                CustomPasswordResetView,
                CustomPasswordResetDoneView,
                CustomPasswordResetConfirmView,
                CustomPasswordResetCompleteView
)

urlpatterns = [
    path("", home, name='home'),
    path("logout", signout, name='logout'),
    path("my_courses", my_courses, name='my_courses'),
    path("signup", SignupView.as_view(), name='Signup'),
    path("login", LoginView.as_view(), name='login'),
    path("contact_us/", contact_us, name='contact_us'), 
    path("explore_courses", explore_courses, name='explore_courses'),
    path("courses/<str:slug>", course_page, name='course_page'),
    path("checkout/<str:slug>", checkout, name='checkout_page'),
    path("verify_payment", verifypayment, name='verify_payment'),
    
    path("reset_password/",CustomPasswordResetView.as_view(template_name = "courses/password_reset.html"),
         name='password_reset'),
    path("reset_password_sent/",CustomPasswordResetDoneView.as_view(template_name = "courses/password_reset_sent.html"), 
         name='password_reset_done'),
    path("reset/<uidb64>/<token>/",CustomPasswordResetConfirmView.as_view(template_name = "courses/password_reset_form.html"),
         name='password_reset_confirm'),
    path("reset_password_complete/",CustomPasswordResetCompleteView.as_view(template_name = "courses/password_reset_complete.html"),
         name='password_reset_complete'),
]
