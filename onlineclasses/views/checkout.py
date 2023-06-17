from time import time
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from onlineclasses.models import Course,Payment,Usercourse
from myproject.settings import *
import razorpay
client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

def checkout(request,slug):
    course = Course.objects.get(slug=slug)
    if(request.user.is_authenticated is False):
        return redirect('login')
    user = request.user
    action = request.GET.get('action')
    order = None
    payment = None
    error = None
    if action == 'create_payment':
        
        try:
            user_course = Usercourse.objects.get(user=user,course=course)
            error = "You are already enrolled in this course"
        except:
            pass
        if error is None:
            discounted_price = course.price * (1 - course.discount * 0.01)
            amount = max(int(discounted_price * 100), 1)

            currency ="INR"
            #receipt =
            notes ={
                'email': user.email,
                'name': f'{user.first_name} {user.last_name}'
            } 
            receipt = f"RKMVCC-{int(time())}"
            order = client.order.create(
                {
                'receipt': receipt,
                'notes': notes,
                'amount': amount,
                'currency':currency
                }
            )
            
            payment = Payment()
            payment.user = user
            payment.course = course
            payment.order_id = order['id']
            payment.save()
    context = {
        'course':course,
        'order':order,
        'payment':payment,
        'user':user,
        'error':error
    }
    return render(request,template_name= "courses/checkout.html",context=context)

@csrf_exempt
def verifypayment(request):
    if request.method == 'POST':
        print(request.POST)
        data = request.POST
        context = {}
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']
            
            
            payment = Payment.objects.get(order_id = razorpay_order_id)
            payment.payment_id = razorpay_payment_id
            payment.status = True
            
            userCourse = Usercourse(user = payment.user,course = payment.course)
            userCourse.save()
            
            payment.user_course = userCourse
            payment.save()
            login(request,payment.user)
            
            return redirect('my_courses')
        except:
            return HttpResponse("Invalid Payment details")
