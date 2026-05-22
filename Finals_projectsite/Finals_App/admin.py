from django.contrib import admin
from .models import Profile, Course, Room, Semester, Enrolled, Schedule

admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Room)
admin.site.register(Semester)
admin.site.register(Enrolled)
admin.site.register(Schedule)
