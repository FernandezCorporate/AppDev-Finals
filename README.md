# PEF Scheduling System
### Personal Evaluation Form — Course Scheduling Web Application with Grade Calculator
*Built with Django | For BSIT Students*

---

## 1. Project Overview

The **PEF Scheduling System** is a web application designed to digitize and streamline the arrangement of course schedules from the Personal Evaluation Form (PEF) for Bachelor of Science in Information Technology (BSIT) students. The PEF is a semestral document that is handed to students after enrollment, which contains their enrolled courses, assigned instructors, time schedules, and room assignments.

### The Problem
Currently, the generated PEF document lacks chronological organization. This structural flaw forces students to manually rearrange their weekly timelines using external spreadsheet tools or third-party scheduling software. This manual process introduces significant pain points:
* **High Error Margins:** Manual data entry frequently leads to scheduling oversights, room conflicts, and time overlaps.
* **Inflexible Adjustments:** Mid-semester schedule updates and section changes are common within the BSIT program, making static spreadsheets difficult and tedious to maintain.
* **Inefficient Workflows:** Students waste valuable academic time duplicating data across platforms just to visualize their weekly routines.

### The Solution
The **PEF Scheduling System** addresses these inefficiencies by introducing an automated, centralized web platform. 
* **Automated Chronological Sorting:** Users shall only need to input data from their PEF, and the system will automatically reorganize it into a proper chronological order.
* **Interactive Schedule Visualization:** Students are provided with an intuitive, user-friendly table, which can be toggled into a calendar interface that updates dynamically.
* **Grade Calculator:** The application also provides a grade calculator, allowing students to view a forecast of their expected GWA (general weighted average).
---

## 2. Features

### Semester Management
- Create, view, edit, and delete semesters (e.g., 1st Semester 2024–2025).
- Each semester is linked to a specific user account for data privacy.
- Semesters are displayed as cards on the home dashboard for quick navigation.

### Course Enrollment
- Enroll courses into a specific semester using a predefined course list from the BSIT prospectus.
- Assign a teacher (first name and last name) to each enrolled course.
- Record the final grade upon completion of the semester.
- Courses are validated against unique constraints to prevent duplicate enrollment within the same semester.

### Schedule Management
- Add one or more schedule entries per enrolled course (supports split schedules across multiple days).
- Schedule entries include day of the week, start time, end time, and room assignment.
- Schedules are managed inline within the course enrollment form using a formset.
- A visual calendar grid displays all schedules for a semester, with pixel-precise positioning based on start and end times.

### Grade Calculator
- Select a semester and input final grades for each enrolled course.
- Automatically computes the General Weighted Average (GWA) based on course units.
- NSTP courses are automatically excluded from the GWA computation.

### Holiday Viewer
- Fetches public holidays for a given year and country using the Nager.Date public API.
- Defaults to Philippine holidays (PH) but supports any valid country code.

### Course Reference
- Courses are pre-loaded from the official BSIT prospectus and are not created ad hoc.
- Each course entry includes a course code, descriptive title, lecture units, and laboratory units.

### User Authentication
- Each user's data is isolated — a logged-in user can only view and manage their own semesters and PEF records.
- Utilizes Google OAuth client for user authentication, which only supports registered email accounts under the Palawan State University domain.

---

## 3. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | Django (Python) | MVC framework, ORM, views |
| Frontend | HTML / CSS / JavaScript / Bootstrap | Responsive UI, templates |
| Form Styling | django-widget-tweaks | Custom form field rendering |
| Database | SQLite (dev) / PostgreSQL | Data persistence |
| Auth | Google OAuth | User login and isolation |
| External API | Nager.Date API | Public holiday data |

---

## 4. Data Models

All models extend a `BaseModel` that provides `created_at` and `updated_at` timestamps.

### Course
A read-only reference table pre-populated by the user admin with courses from the BSIT prospectus. Students and officers do not create courses — they select from this list.

| Field | Type | Description |
|---|---|---|
| course_code | CharField | Unique course identifier (e.g., IT101) |
| title | CharField | Full descriptive name of the course |
| lec_units | IntegerField | Number of lecture units |
| lab_units | IntegerField | Number of laboratory units |

### Semester
Represents an academic semester belonging to a user. Acts as the top-level container for all enrolled courses and their schedules.

| Field | Type | Description |
|---|---|---|
| semester_name | CharField | e.g., 1st Semester, 2nd Semester |
| year_start | IntegerField | Start year of the academic year |
| year_end | IntegerField | End year of the academic year |
| user | ForeignKey (User) | Owner of this semester record |

### Enrolled
A junction record linking a `Course` to a `Semester` with additional metadata such as teacher assignment and final grade. Enforces a unique constraint preventing the same course from being enrolled twice in the same semester.

| Field | Type | Description |
|---|---|---|
| course | ForeignKey (Course) | The course being enrolled |
| semester | ForeignKey (Semester) | The semester this enrollment belongs to |
| teacher_fname | CharField | First name of the assigned teacher |
| teacher_lname | CharField | Last name of the assigned teacher |
| final_grade | DecimalField | Final grade (optional, filled after semester ends) |

### Schedule
Stores the time-slot information for an enrolled course. One enrolled course can have multiple schedule entries to accommodate split schedules (e.g., lecture on Monday, laboratory on Wednesday).

| Field | Type | Description |
|---|---|---|
| enrolled | ForeignKey (Enrolled) | Parent enrolled record |
| day_of_week | CharField (choices) | Monday through Sunday |
| start_time | TimeField | Class start time |
| end_time | TimeField | Class end time |
| room | CharField | Room or venue assignment |

---

## 5. Application Views

| View | Type | Description |
|---|---|---|
| HomePageView | ListView | Displays the user's semesters as cards |
| SemesterDetailView | DetailView | Shows a visual calendar grid of all schedules for a semester |
| SemesterCreateView | CreateView | Creates a new semester; auto-attaches the logged-in user |
| SemesterUpdateView | UpdateView | Edits semester name and year range |
| SemesterDeleteView | DeleteView | Deletes a semester and all its related records |
| EnrolledCreateView | CreateView | Adds a course to a semester with an inline schedule formset |
| EnrolledUpdateView | UpdateView | Edits an enrolled course and its inline schedules |
| EnrolledDeleteView | DeleteView | Removes an enrolled course and its schedules |
| holiday_api_view | Function view | Fetches and displays public holidays via external API |
| grade_calculator_view | Function view | Computes GWA from enrolled courses and inputted grades |

---

## 6. Installation & Setup

The application is deployed and accessible at:
https://siteschedulergradecalculator.pythonanywhere.com

*Note: The web application is strictly for psu.edu.palawan emails only*

---

## 7. Authors

| Name | Role |
|---|---|
| [Ralph Justine S. Beronio](https://github.com/flenggo) | Frontend Developer |
| [Allen Glenn F. Fernandez](https://github.com/FernandezCorporate) | Backend Developer |
| [Alliah E. Mahilum](https://github.com/alliah2025) | Frontend Developer |
| [Mycka P. Valoroso](https://github.com/mycka4) | Backend Developer |

---

## 8. License

This project was developed as an academic requirement. All rights reserved by the authors. Unauthorized reproduction or distribution without prior consent is prohibited.


## 9. For the Instructor

During the development of the web application, there were complications that have arised on the last phases of the project (google authentication).

Specifically, the SITE ID for the localhost and pythonanywhere sites does not match for the admin when hosted locally and when accessed through the pythonanywhere. Thus, the code in settings.py for this remote repository is different from those uploaded in pythonanywhere.  

**For the remote repo:**
```
if "pythonanywhere" in socket.gethostname():
    SITE_ID = 4
else:
    SITE_ID = 3
```  

**For the pythonanywhere repo:**
```
SITE_ID = 5
```

To avoid merge conflicts, the developers have also opted to finish the last feature on the application by manually coding it on pythonanywhere. This feature was the login persistence using *LoginRequiredMixin* for **class-based views** and *@login_required* decorator for **function-based views**. Hence, these keywords may not be present for the views.py file of this remote repository.

Additionally, there has also been an oversight with the models of the application, specifically  for *Schedule*. On its meta, it has:
`unique_together = ('day_of_week', 'start_time', 'room')`

This creates a bug where it prevents other users from enterring a new schedule if the specific combination of day, start time, and room is already existing on the database. As observed, this is illogical since it would be common for multiple students (classmates) to input the same combination of the mentioned information.
