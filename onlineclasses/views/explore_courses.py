from django.shortcuts import render
from onlineclasses.models import Course
def explore_courses(request):
    courses = Course.objects.all()
    print(courses)
    return render(request, template_name='courses/explore_courses.html',context={"courses": courses})
