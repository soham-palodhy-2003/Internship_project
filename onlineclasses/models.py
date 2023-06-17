from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100,default='Default Title')

    def __str__(self):
        return self.title
class Course(models.Model):
    title = models.CharField(max_length=100,null=False)
    slug = models.CharField(max_length=100,null=False,unique=True)
    description = models.TextField(max_length=500,null=True)
    duration = models.PositiveIntegerField(help_text="Duration:")
    price = models.IntegerField(null=False)
    discount = models.PositiveIntegerField(null=False, default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    length = models.PositiveIntegerField(null=False)
    
    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Class(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    starting_time = models.DateTimeField()
    ending_time = models.DateTimeField()
    
    def __str__(self):
        return self.title
    

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Usercourse(models.Model):
    user = models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,null=False,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} {self.course.title}'
    
class Payment(models.Model):
    order_id = models.CharField(max_length=50,null=True)
    payment_id = models.CharField(max_length=50,null=True)
    user_course = models.ForeignKey(Usercourse,null=True,blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    
class Recording(models.Model):
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
   # video_file = models.FileField(upload_to='recordings/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
