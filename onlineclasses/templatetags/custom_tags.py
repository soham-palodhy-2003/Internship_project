from django import template
import math
from onlineclasses.models import Usercourse,Course
register = template.Library()
@register.simple_tag

def cal_sale_price(price,discount):
    if discount is None or discount == 0:
        return price
    sellPrice = price-(price * (discount * 0.01))
    return math.floor(sellPrice)

@register.filter
def rupee(price):
    rupee_price = price 
    return f'₹{rupee_price}'

@register.simple_tag

def is_enrolled(request,course):
    user = None
    if not request.user.is_authenticated:
        return False
    user = request.user
    try:
        user_course = Usercourse.objects.get(user=user,course=course)
        return True
    except:
        return False
