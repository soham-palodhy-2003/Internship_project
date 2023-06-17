from django.contrib import admin
from .models import UserProfile,Course,Lesson,Class,Enrollment,Payment,Usercourse,Recording
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Class)
admin.site.register(Enrollment)
admin.site.register(Payment)
admin.site.register(Usercourse)
admin.site.register(Recording)
