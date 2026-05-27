from django.shortcuts import render
from django.views.generic import ListView
from Finals_App.models import Semester

class SemesterListView(ListView):
    model = Semester
    template_name = 'home.html'
    context_object_name = 'semesters'