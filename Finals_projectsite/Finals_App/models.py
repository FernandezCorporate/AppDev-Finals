from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Course(BaseModel):
    course_code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    lec_units = models.IntegerField()
    lab_units = models.IntegerField()

    def __str__(self):
        return f"{self.course_code} - {self.title}"


class Room(BaseModel):
    name = models.CharField(max_length=10, unique=True)
    building = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.building} {self.name}"


class Semester(BaseModel):
    semester_name = models.CharField(max_length=20)
    school_year = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.semester_name} {self.school_year}"
    

class Enrolled(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    teacher_fname = models.CharField(max_length=255, blank=True, null=True)
    teacher_lname = models.CharField(max_length=255, blank=True, null=True)

    final_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Enrolled"
        unique_together = ('course', 'user', 'semester')

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.course_code} for {self.semester.semester_name} {self.semester.school_year}"

class Schedule(BaseModel):
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_of_week = models.CharField(max_length=20, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ], default='Monday')

    enrolled = models.ForeignKey(Enrolled, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('day_of_week', 'start_time', 'room')

    def __str__(self):
        return f"{self.enrolled.course.course_code} on {self.day_of_week} from {self.start_time} to {self.end_time} in {self.room}"
