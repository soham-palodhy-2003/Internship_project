from django.shortcuts import render

def contact_us(request):
    return render(request, template_name='courses/contact_us.html')
