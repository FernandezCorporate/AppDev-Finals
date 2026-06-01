from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
 
from Finals_App.models import Semester, Enrolled, Schedule, Course

class HomePageView(ListView):
    model = Semester
    template_name = 'home.html'
    context_object_name = 'semesters'
 
    def get_queryset(self):
        # Only show semesters belonging to the logged-in user
        return Semester.objects.filter(user=self.request.user).order_by('-year_start', 'semester_name')

class SemesterDetailView(DetailView):
    model = Semester
    template_name = 'semester_detail.html'
    context_object_name = 'semester'
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all enrolled courses for this semester, with their schedules
        context['enrolled_list'] = (
            Enrolled.objects
            .filter(semester=self.object)
            .prefetch_related('schedule_set', 'course')
            .order_by('course__course_code')
        )
        return context

