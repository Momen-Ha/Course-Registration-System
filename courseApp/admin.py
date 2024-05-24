from django.contrib import admin
from .models import Student, CourseSchedule, Course, StudentReg


class CourseScheduleInline(admin.TabularInline):
    model = CourseSchedule
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseScheduleInline]


# Register your models here.
admin.site.register(Student)
admin.site.register(CourseSchedule)
admin.site.register(Course)
admin.site.register(StudentReg)

