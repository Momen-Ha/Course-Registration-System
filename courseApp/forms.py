from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django import forms


class studentRegForm(ModelForm):
    class Meta:
        model=StudentReg
        fields='__all__'


class createCourseForm(ModelForm):
    class Meta:
        model=Course
        fields='__all__'
        exclude=['scheduleID']


class CourseScheduleForm(forms.ModelForm):
    class Meta:
        model = CourseSchedule
        fields = '__all__'


class createStudentForm(ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    class Meta:
        model=Student
        fields = ['name',]


class editStudentInfoForm(ModelForm):
    class Meta:
        model=Student
        fields = ['name', 'password']


class createNewUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        def save(self, commit=True):
            user = super().save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
                # Create the Student instance
                Student.objects.create(name=user.username, email=user.email, user=user)
            return user
