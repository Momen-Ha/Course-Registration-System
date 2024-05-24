
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('courses/', views.courses, name="courses"),
    path('course/<str:pk>/', views.course, name="course"),
    path('student/<str:pk>', views.student, name="student"),
    path('student/editInfo/<str:pk>', views.editStudentInfo, name="editStudentInfo"),
    path('createStudentReg/', views.createStudentReg, name="createStudentReg"),
    path('editStudentReg/<str:pk>', views.editStudentReg, name="editStudentReg"),
    path('deleteStudentReg/<str:pk>', views.deleteStudentReg, name="deleteStudentReg"),
    path('addCourse/<str:student_id>/<int:course_code>/', views.addCourse, name='addCourse'),
    path('createStudent/', views.createStudent, name="createStudent"),
    path('deleteStudent/<str:pk>', views.deleteStudent, name="deleteStudent"),
    path('editCourse/<str:pk>', views.editCourse, name="editCourse"),
    path('createCourse/', views.createCourse, name="createCourse"),
    path('deleteCourse/<str:pk>', views.deleteCourse, name="deleteCourse"),
    path('register/', views.register, name="register"),
    path('login/', views.UserLogin, name="login"),
    path('logout/', views.userLogout, name="logout"),
    
]