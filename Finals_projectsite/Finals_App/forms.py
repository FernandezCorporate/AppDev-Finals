from django.forms import ModelForm
from django import forms
from .models import Enrolled, Schedule
 
 
class EnrolledForm(ModelForm):
    class Meta:
        model = Enrolled
        # Exclude 'semester' because it is injected by the view via the URL
        fields = ['course', 'teacher_fname', 'teacher_lname', 'final_grade']
 
 
class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        # Exclude 'enrolled' because it is injected by the view via the URL
        fields = ['day_of_week', 'start_time', 'end_time', 'room']
 