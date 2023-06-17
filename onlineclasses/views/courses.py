from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from onlineclasses.models import Course,Usercourse
from django.contrib.auth.decorators import login_required

def course_page(request,slug):
    course = Course.objects.get(slug=slug)
    context = {
        "course": course
    }
    return render(request,template_name= "courses/course_page.html",context=context)
@login_required(login_url="login")
def my_courses(request):
    user = request.user
    user_course = Usercourse.objects.filter(user = user)
    context ={
        'user_course': user_course
    }
    return render(request, template_name="courses/my_courses.html",context=context)