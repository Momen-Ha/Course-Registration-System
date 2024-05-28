from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.db.models import Count
from .models import *
from .forms import *
from .filters import * 
from .decorators import *
from django.contrib.auth.models import Group
# Create your views here.


@forAdmins
@login_required(login_url='login')    
def home(request):
    courses = Course.objects.all()
    students = Student.objects.all()
    student_regs = StudentReg.objects.select_related('student', 'course__scheduleID')
    studentsNumber = students.count()
    coursesNumber = courses.count()

    context = {
        "students":students,
        "studentsSchedule": student_regs,
        "studentsNumber": studentsNumber,
        "coursesNumber": coursesNumber,
    }
    return render(request, 'courseApp/dashboard.html', context)



@login_required(login_url='login')    
def student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if not student:
        return HttpResponse("Student not found")
    student_registrations = student.studentreg_set.all()

    # Collect the course codes from student registrations
    registered_course_codes = student_registrations.values_list('course__code', flat=True)

    # Uncompleted courses with student count excluding completed students
    uncompleted_courses = student_registrations.filter(completed=False).select_related('course__scheduleID').annotate(
        registered_students_count=Count('course__studentreg', filter=Q(course__studentreg__completed=False))
    )
    
    completed_courses = student_registrations.filter(completed=True).select_related('course')
    
     # Filter available courses based on the specified conditions
    available_courses = Course.objects.exclude(code__in=registered_course_codes).filter(
    Q(prerequisites__isnull=True) | Q(
        Q(prerequisites__studentreg__student=student) &
        Q(prerequisites__studentreg__completed=True)
),
    scheduleID__isnull=False,
    ).filter(~Q(scheduleID__days = None)).distinct().annotate(
    registered_students_count=models.Count('studentreg')
    ).filter(
    capacity__gt=models.F('registered_students_count')
    )

    course_filter = courseFilter(request.GET, queryset=available_courses)
    available_courses = course_filter.qs

    context = {
        "student": student,
        "registrations": student_registrations,
        "uncompleted_courses": uncompleted_courses,
        "completed_courses": completed_courses,
        "available_courses": available_courses,
        "course_filter": course_filter,
    }
    return render(request, 'courseApp/student.html', context)

@login_required(login_url='login')
def courses(request):

    course = Course.objects.select_related().annotate(
    registered_students_count=Count('studentreg', filter=Q(studentreg__completed=False))
    ).order_by('code')

    searchFilter = courseFilter(request.GET, queryset=course)
    course = searchFilter.qs
    context = {
        "Course":course,
        "searchFilter": searchFilter
    }
    return render(request, "courseApp/courses.html", context)


@login_required(login_url='login')
def courseSchedules(request):
    schedules = CourseSchedule.objects.all()
    return render(request, "courseApp/dashboard.html", schedules)


@login_required(login_url='login')
def course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, "courseApp/course.html", {"Course":course})


@forAdmins
@login_required(login_url='login')
def editStudentInfo(request, pk):
    student = Student.objects.get(id=pk)
    form = editStudentInfoForm(instance=student)
    if request.method == 'POST':
        form = editStudentInfoForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect(reverse('student', args=[student.id]))
    context = {"form": form, "student": student}
    return render(request, "courseApp/editStudentInfo.html", context)


@forAdmins
@login_required(login_url='login')
def deleteStudent(request, pk):
    student = Student.objects.get(id=pk)
    user = student.user
    if request.method == 'POST':
        user.delete()
        return redirect('/')
    context={"course": student}
    return render(request, "courseApp/deleteStudent.html", context)


@forAdmins
def createStudent(request):
    form = createStudentForm()
    if request.method == 'POST':
        form = createStudentForm(request.POST)
        if(form.is_valid()):
            #create the user
            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Email already exists')
            else:

                # Create the user
                user = User.objects.create_user(username=username, password=password, email=email)
                # Create the student and link to the user
                student = Student.objects.create(user=user, name=name, email=email, password=password)
                group = Group.objects.get(name="students")
                user.groups.add(group)
                messages.success(request, f'Student {name} created successfully')
                return redirect('/')
    else:
        form = createStudentForm()
    context = {"form": form}
    return render(request, "courseApp/createStudent.html", context)




@forAdmins
@login_required(login_url='login')
def createStudentReg(request):
    form = studentRegForm()
    if request.method == 'POST':
        form = studentRegForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {"form":form}
    return render(request, "courseApp/studentRegForm.html", context)

@forAdmins
@login_required(login_url='login')
def editStudentReg(request, pk):
    reg = StudentReg.objects.get(id=pk)
    form = studentRegForm(instance=reg)
    if request.method == 'POST':
        form = studentRegForm(request.POST, instance=reg)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {"form": form}
    return render(request, "courseApp/editStudentReg.html", context)


@login_required(login_url='login')
def deleteStudentReg(request, pk):
    reg = StudentReg.objects.get(id=pk)
    if request.method == 'POST':
        reg.delete()
        return redirect(reverse('student', args=[reg.student.id]))
    context={"reg": reg}
    return render(request, "courseApp/deleteRegistration.html", context)



@login_required(login_url='login')
def addCourse(request, student_id, course_code):
    student = get_object_or_404(Student, pk=student_id)
    course = get_object_or_404(Course, code=course_code) 
    
    # Check if the student is already registered for the course
    if StudentReg.objects.filter(student=student, course=course, completed=False).exists():
        return redirect('student', pk=student_id)
    
    newCourseSchedule = course.scheduleID    
    studentCourses = student.studentreg_set.filter(completed=False).select_related('course__scheduleID')
    
    for reg in studentCourses:
        reg_course_schedule = reg.course.scheduleID
        if reg_course_schedule.days == newCourseSchedule.days and \
            (newCourseSchedule.startTime < reg_course_schedule.endTime and newCourseSchedule.endTime > reg_course_schedule.startTime):
            messages.error(request, f'Time conflict with course: {reg.course.name}')
            return render(request, 'courseApp/addCourse.html', {'student': student, 'course': course, 'conflict': True})
    
    if request.method == 'POST':
        # If no conflicts, add the course to the student's schedule
        StudentReg.objects.create(student=student, course=course, completed=False)
        messages.success(request, 'Course added successfully!')
        return redirect('student', pk=student_id)
    
    context = {
        'student': student,
        'course': course,
        'conflict': False
    }
    return render(request, 'courseApp/addCourse.html', context)

@forAdmins
@login_required(login_url='login')
def deleteCourse(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, f'Course {course.name} was deleted successfully.')
        return redirect('courses') 
    
    context = {
        'course': course,
    }
    return render(request, 'courseApp/deleteCourse.html', context)


@forAdmins
@login_required(login_url='login')
def createCourse(request):
    course_form = createCourseForm(request.POST)
    if request.method == 'POST':
        course_form = createCourseForm(request.POST)
        schedule_form = CourseScheduleForm(request.POST)
        
        if course_form.is_valid() and schedule_form.is_valid():
            schedule = schedule_form.save()
            course = course_form.save(commit=False)
            course.scheduleID = schedule
            course.save()
            return redirect('courses')  # Redirect to a success page or course list

    else:
        course_form = createCourseForm()
        schedule_form = CourseScheduleForm()

    context = {
        'course_form': course_form,
        'schedule_form': schedule_form,
    }
    return render(request, 'courseApp/createCourse.html', context)
        


@forAdmins
@login_required(login_url='login')
def editCourse(request, pk):
    course = get_object_or_404(Course, pk=pk)
    
    # If the course has a schedule, load it, otherwise create an empty one
    schedule = course.scheduleID if course.scheduleID else CourseSchedule()

    if request.method == 'POST':
        course_form = createCourseForm(request.POST, instance=course)
        schedule_form = CourseScheduleForm(request.POST, instance=schedule)

        if course_form.is_valid() and schedule_form.is_valid():
            schedule = schedule_form.save()
            course = course_form.save(commit=False)
            course.scheduleID = schedule
            course.save()
            return redirect('courses')
    else:
        course_form = createCourseForm(instance=course)
        schedule_form = CourseScheduleForm(instance=schedule)

    context = {
        'course_form': course_form,
        'schedule_form': schedule_form,
    }
    return render(request, "courseApp/createCourse.html", context)



@notLoggedUser
def register(request):
    form = createNewUser()
    if request.method == 'POST':
        form = createNewUser(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            group = Group.objects.get(name="students")
            user.groups.add(group)
            # create student instance
            Student.objects.create(name=username, email=email, user=user)
            messages.success(request, username + " created successfully")
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = createNewUser()
    
    context = {
        'form': form
    }
    return render(request, 'courseApp/register.html', context)
    


@notLoggedUser
def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user= authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Invalid username or password.")
    return render(request, "courseApp/login.html")
 


@login_required(login_url='login')
def userLogout(request):
    logout(request)
    return redirect('login')
