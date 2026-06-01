from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from Finals_App.models import Semester, Enrolled, Schedule
from Finals_App.forms import EnrolledForm, ScheduleForm


class HomePageView(ListView):
    model = Semester
    template_name = 'home.html'
    context_object_name = 'semesters'

    def get_queryset(self):
        return Semester.objects.filter(user=self.request.user).order_by('-year_start', 'semester_name')

class SemesterDetailView(DetailView):
    model = Semester
    template_name = 'semester_detail.html'
    context_object_name = 'semester'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrolled_list'] = (
            Enrolled.objects
            .filter(semester=self.object)
            .prefetch_related('schedule_set', 'course')
            .order_by('course__course_code')
        )
        return context

class SemesterCreateView(CreateView):
    model = Semester
    fields = ['semester_name', 'year_start', 'year_end']
    template_name = 'semester_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):

        form.instance.user = self.request.user
        return super().form_valid(form)


class SemesterUpdateView(UpdateView):
    model = Semester
    fields = ['semester_name', 'year_start', 'year_end']
    template_name = 'semester_form.html'
    success_url = reverse_lazy('home')


class SemesterDeleteView(DeleteView):
    model = Semester
    template_name = 'semester_del.html'
    success_url = reverse_lazy('home')

class EnrolledCreateView(CreateView):
    model = Enrolled
    form_class = EnrolledForm
    template_name = 'enrolled_form.html'
    success_url = reverse_lazy('home')


class EnrolledUpdateView(UpdateView):
    model = Enrolled
    form_class = EnrolledForm
    template_name = 'enrolled_form.html'
    success_url = reverse_lazy('home')


class EnrolledDeleteView(DeleteView):
    model = Enrolled
    template_name = 'enrolled_del.html'
    success_url = reverse_lazy('home')

class ScheduleCreateView(CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'schedule_form.html'
    success_url = reverse_lazy('home')


class ScheduleUpdateView(UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'schedule_form.html'
    success_url = reverse_lazy('home')


class ScheduleDeleteView(DeleteView):
    model = Schedule
    template_name = 'schedule_del.html'
    success_url = reverse_lazy('home')