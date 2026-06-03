from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from collections import defaultdict
from datetime import datetime
from django.db.models import Q

import requests

from Finals_App.models import Semester, Enrolled, Schedule
from Finals_App.forms import EnrolledForm, ScheduleFormSet


# ---------------- HOME ----------------
class HomePageView(ListView):
    model = Semester
    template_name = 'home.html'
    context_object_name = 'semesters'

    def get_queryset(self):
        return Semester.objects.filter(
            user=self.request.user
        ).order_by('-year_start', 'semester_name')


# ---------------- SEMESTER DETAIL ----------------
class SemesterDetailView(DetailView):
    model = Semester
    template_name = 'semester_detail.html'
    context_object_name = 'semester'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        day_order = [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday'
        ]

        grouped = defaultdict(list)

        schedules = Schedule.objects.filter(
            enrolled__semester=self.object
        ).select_related(
            'enrolled__course'
        ).order_by(
            'day_of_week',
            'start_time'
        )

        PIXELS_PER_MINUTE = 1.2
        START_HOUR = 7

        calendar_events = []

        for sched in schedules:

            grouped[sched.day_of_week].append(sched)

            start_minutes = (
                sched.start_time.hour * 60 +
                sched.start_time.minute
            )

            end_minutes = (
                sched.end_time.hour * 60 +
                sched.end_time.minute
            )

            base_minutes = START_HOUR * 60

            top = (
                start_minutes - base_minutes
            ) * PIXELS_PER_MINUTE

            height = (
                end_minutes - start_minutes
            ) * PIXELS_PER_MINUTE

            calendar_events.append({
                'day': sched.day_of_week,
                'top': top,
                'height': height,
                'code': sched.enrolled.course.course_code,
                'title': sched.enrolled.course.title,
                'room': sched.room,
                'start_time': sched.start_time,
                'end_time': sched.end_time,
            })

        context['calendar_events'] = calendar_events

        context['days'] = [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday'
        ]

        context['hours'] = [
            '7:00 AM',
            '8:00 AM',
            '9:00 AM',
            '10:00 AM',
            '11:00 AM',
            '12:00 PM',
            '1:00 PM',
            '2:00 PM',
            '3:00 PM',
            '4:00 PM',
            '5:00 PM',
            '6:00 PM',
            '7:00 PM',
            '8:00 PM'
        ]

        context['grouped_schedules'] = {
            day: grouped[day]
            for day in day_order
            if day in grouped
        }

        return context


# ---------------- SEMESTER CRUD ----------------
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


# ---------------- ENROLLED CREATE ----------------
class EnrolledCreateView(CreateView):
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
class EnrolledUpdateView(UpdateView):
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


class EnrolledDeleteView(DeleteView):
    model = Enrolled
    template_name = 'enrolled_del.html'
    success_url = reverse_lazy('home')

# ---------------- API Views ----------------
def holiday_api_view(request):
    holidays = []
    error = None
    year = datetime.now().year
    country_code = request.GET.get('country_code', 'PH').strip().upper()

    if country_code:
        url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country_code}"

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                holidays = response.json()
            else:
                error = "Invalid country code."
        except Exception:
            error = "Failed to fetch holidays. Please try again later."

    context = {
        "year": year,
        "holidays": holidays,
        "country_code": country_code,
        "error": error
    }

    return render(request, "holidays.html", context)

# ---------------- GRADE CALCULATOR ----------------
def grade_calculator_view(request):
    semesters = Semester.objects.filter(user=request.user)

    selected_semester_id = request.GET.get('semester') or request.POST.get('semester')

    selected_semester = None
    enrolled_list = []
    gwa = None

    if selected_semester_id:
        selected_semester = Semester.objects.filter(
            id=selected_semester_id,
            user=request.user
        ).first()

    if selected_semester:
        enrolled_list = Enrolled.objects.select_related('course').filter(
            semester=selected_semester
        )

    if request.method == "POST" and selected_semester:

        total_units = 0
        total_weighted = 0

        for e in enrolled_list:

            if "NSTP" in e.course.course_code.upper():
                continue

            grade_value = request.POST.get(f'grade_{e.id}')

            if not grade_value:
                continue

            try:
                grade = float(grade_value)
            except ValueError:
                continue

            e.final_grade = grade
            e.save()

        saved_enrolled = Enrolled.objects.select_related('course').filter(
            semester=selected_semester
        )

        for e in saved_enrolled:
            if "NSTP" in e.course.course_code.upper():
                continue

            if e.final_grade is None:
                continue

            units = e.course.lec_units + e.course.lab_units

            total_units += units
            total_weighted += e.final_grade * units

        if total_units > 0:
            gwa = round(total_weighted / total_units, 2)

    return render(request, "grade_calculator.html", {
        "semesters": semesters,
        "enrolled_list": enrolled_list,
        "selected_semester_id": str(selected_semester_id) if selected_semester_id else "",
        "gwa": gwa,
    })