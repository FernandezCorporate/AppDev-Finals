from django import forms
from django.forms import ModelForm, inlineformset_factory
from .models import Enrolled, Schedule


class EnrolledForm(ModelForm):
    class Meta:
        model = Enrolled
        fields = ['course', 'teacher_fname', 'teacher_lname', 'final_grade']
        widgets = {
            'course': forms.Select(attrs={
                'class': 'form-control'
            }),
            'teacher_fname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Juan'
            }),
            'teacher_lname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Dela Cruz'
            }),
            'final_grade': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 1.25',
                'step': '0.01'
            }),
        }


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['day_of_week', 'start_time', 'end_time', 'room']
        widgets = {
            'day_of_week': forms.Select(attrs={
                'class': 'form-select'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'room': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Room 101'
            }),
        }


ScheduleFormSet = inlineformset_factory(
    Enrolled,
    Schedule,
    form=ScheduleForm,      
    fields=['day_of_week', 'start_time', 'end_time', 'room'],
    extra=1,
    can_delete=True
)