from django.contrib import admin
from .models import Course, Semester, Enrolled, Schedule

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'title', 'lec_units', 'lab_units')
    search_fields = ('course_code', 'title')
    list_filter = ('lec_units', 'lab_units')

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('semester_name', 'school_year')
    search_fields = ('semester_name', 'school_year')
    list_filter = ('semester_name', 'school_year')

@admin.register(Enrolled)
class EnrolledAdmin(admin.ModelAdmin):
    list_display = ('course', 'semester', 'teacher_fname', 'teacher_lname')
    search_fields = ('course__course_code', 'semester__semester_name')
    list_filter = ('semester',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('enrolled', 'day_of_week', 'start_time', 'end_time', 'room')
    search_fields = ('enrolled__course__course_code', 'enrolled__semester__semester_name')
    list_filter = ('day_of_week',)