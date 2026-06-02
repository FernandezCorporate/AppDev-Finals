from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin

from Finals_App.models import Semester, Enrolled, Schedule
from Finals_App.forms import EnrolledForm, ScheduleFormSet


# ---------------- HOME ----------------
class HomePageView(LoginRequiredMixin, ListView):
    model = Semester
    template_name = 'home.html'
    context_object_name = 'semesters'

    def get_queryset(self):
        return Semester.objects.filter(
            user=self.request.user
        ).order_by('-year_start', 'semester_name')


# ---------------- SEMESTER DETAIL ----------------
class SemesterDetailView(LoginRequiredMixin, DetailView):
    model = Semester
    template_name = 'semester_detail.html'
    context_object_name = 'semester'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        day_order = [
            'Monday','Tuesday','Wednesday',
            'Thursday','Friday','Saturday','Sunday'
        ]

        grouped = defaultdict(list)

        schedules = Schedule.objects.filter(
            enrolled__semester=self.object
        ).select_related('enrolled__course').order_by('start_time')

        for s in schedules:
            grouped[s.day_of_week].append(s)

        context['grouped_schedules'] = {
            day: grouped[day]
            for day in day_order if day in grouped
        }

        return context


# ---------------- SEMESTER CRUD ----------------
class SemesterCreateView(LoginRequiredMixin, CreateView):
    model = Semester
    fields = ['semester_name', 'year_start', 'year_end']
    template_name = 'semester_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SemesterUpdateView(LoginRequiredMixin, UpdateView):
    model = Semester
    fields = ['semester_name', 'year_start', 'year_end']
    template_name = 'semester_form.html'
    success_url = reverse_lazy('home')


class SemesterDeleteView(LoginRequiredMixin, DeleteView):
    model = Semester
    template_name = 'semester_del.html'
    success_url = reverse_lazy('home')


# ---------------- ENROLLED CREATE ----------------
class EnrolledCreateView(LoginRequiredMixin, CreateView):
    model = Enrolled
    form_class = EnrolledForm
    template_name = 'enrolled_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.semester = Semester.objects.get(
            pk=self.kwargs['semester_pk']
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['schedule_formset'] = ScheduleFormSet(self.request.POST)
        else:
            context['schedule_formset'] = ScheduleFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['schedule_formset']

        if not formset.is_valid():
            return self.form_invalid(form)

        form.instance.semester = self.semester
        self.object = form.save()

        formset.instance = self.object
        formset.save()

        return redirect('semester-detail', pk=self.semester.pk)


# ---------------- ENROLLED UPDATE ----------------
class EnrolledUpdateView(LoginRequiredMixin, UpdateView):
    model = Enrolled
    form_class = EnrolledForm
    template_name = 'enrolled_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['schedule_formset'] = ScheduleFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            context['schedule_formset'] = ScheduleFormSet(
                instance=self.object
            )

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['schedule_formset']

        if not formset.is_valid():
            return self.form_invalid(form)

        self.object = form.save()

        formset.instance = self.object
        formset.save()

        return redirect('semester-detail', pk=self.object.semester.pk)


class EnrolledDeleteView(LoginRequiredMixin, DeleteView):
    model = Enrolled
    template_name = 'enrolled_del.html'
    success_url = reverse_lazy('home')