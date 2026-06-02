from django.forms import ModelForm, inlineformset_factory
from .models import Enrolled, Schedule


class EnrolledForm(ModelForm):
    class Meta:
        model = Enrolled
        fields = [
            'course',
            'teacher_fname',
            'teacher_lname',
            'final_grade'
        ]


ScheduleFormSet = inlineformset_factory(
    Enrolled,
    Schedule,
    fields=[
        'day_of_week',
        'start_time',
        'end_time',
        'room'
    ],
    extra=1,
    can_delete=True
)