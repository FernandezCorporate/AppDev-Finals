from django.contrib import admin
from django.urls import path
from Finals_App import views

from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.HomePageView.as_view(), name='home'),

    path('semester/<int:pk>/', views.SemesterDetailView.as_view(), name='semester-detail'),

    path('semester/create/', views.SemesterCreateView.as_view(), name='semester-create'),
    path('semester/<int:pk>/update/', views.SemesterUpdateView.as_view(), name='semester-update'),
    path('semester/<int:pk>/delete/', views.SemesterDeleteView.as_view(), name='semester-delete'),

    path(
        'semester/<int:semester_pk>/enrolled/create/',
        views.EnrolledCreateView.as_view(),
        name='enrolled-create'
    ),

    path(
        'enrolled/<int:pk>/update/',
        views.EnrolledUpdateView.as_view(),
        name='enrolled-update'
    ),

    path(
        'enrolled/<int:pk>/delete/',
        views.EnrolledDeleteView.as_view(),
        name='enrolled-delete'
    ),

    path('holidays/', views.holiday_api_view, name='holiday-api'),
    path('grade-calculator/', views.grade_calculator_view, name='grade-calculator'),

    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/javascript'), name='sw.js'),
]