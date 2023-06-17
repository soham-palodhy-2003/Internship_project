from onlineclasses.views.homepage import home
from onlineclasses.views.courses import course_page,my_courses
from onlineclasses.views.checkout import checkout,verifypayment
from onlineclasses.views.explore_courses import explore_courses
from onlineclasses.views.auth import SignupView
from onlineclasses.views.auth import LoginView,signout
from onlineclasses.views.auth import CustomPasswordResetView,CustomPasswordResetDoneView,CustomPasswordResetConfirmView,CustomPasswordResetCompleteView

__all__ = [
    'home',
    'SignupView',
    'LoginView',
    'signout',
    'explore_courses',
    'checkout',
    'verifypayment',
    'CustomPasswordResetView',
    'CustomPasswordResetDoneView',
    'CustomPasswordResetConfirmView',
    'CustomPasswordResetCompleteView',

]