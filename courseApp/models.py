from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.db import models


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class CourseSchedule(models.Model):
    days = models.CharField(max_length=50,null=True, blank=True)
    startTime = models.TimeField(null=True, blank=True)
    endTime = models.TimeField(null=True, blank=True)
    roomNo = models.CharField(max_length=10, null=True, blank=True)
    
    def __str__(self):
        return f"Schedule for {self.days} from {self.startTime} to {self.endTime}"

class Course(models.Model):
    code = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField( null=True)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='prerequisite_for')
    instructor = models.CharField(max_length=100)
    capacity = models.IntegerField()
    scheduleID = models.ForeignKey(CourseSchedule,null=True,blank=True,default='', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class StudentReg(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.id} : {self.student.name} : {self.course.name}"
