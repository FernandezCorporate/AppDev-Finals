"""
URL configuration for Finals_projectsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Finals_App.views import HomePageView
from Finals_App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='home'),
    path('semester/<int:pk>/', views.SemesterDetailView.as_view(), name='semester-detail'),
    path('semester/create/', views.SemesterCreateView.as_view(), name='semester-create'),
    path('semester/<int:pk>/update/', views.SemesterUpdateView.as_view(), name='semester-update'),
    path('semester/<int:pk>/delete/', views.SemesterDeleteView.as_view(), name='semester-delete'),
    path('enrolled/create/', views.EnrolledCreateView.as_view(), name='enrolled-create'),
    path('enrolled/<int:pk>/update/', views.EnrolledUpdateView.as_view(), name='enrolled-update'),
    path('enrolled/<int:pk>/delete/', views.EnrolledDeleteView.as_view(), name='enrolled-delete'),
    path('schedule/create/', views.ScheduleCreateView.as_view(), name='schedule-create'),
    path('schedule/<int:pk>/update/', views.ScheduleUpdateView.as_view(), name='schedule-update'),
    path('schedule/<int:pk>/delete/', views.ScheduleDeleteView.as_view(), name='schedule-delete'),
]
