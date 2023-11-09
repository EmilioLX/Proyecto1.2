from django.urls import path
from .views import HomeView, RegisterView, ProfileView, CoursesView, CourseCreateView, CourseEditView, CourseDeleteView, CourseEnrollmentView, StudentListMarkView, UpdateMarkView, evolution
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView,  PasswordResetDoneView

urlpatterns = [
    # PAGINA DE INICIO
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', login_required(ProfileView.as_view()), name='profile'),
    path('courses/', CoursesView.as_view(), name='courses'),
    path('courses/create/', login_required(CourseCreateView.as_view()), name='course_create'),
    path('courses/<int:pk>/edit/', login_required(CourseEditView.as_view()), name='course_edit'),
    path('courses/<int:pk>/delete/', login_required(CourseDeleteView.as_view()), name='course_delete'),
    path('enroll_course/<int:course_id>', login_required(CourseEnrollmentView.as_view()), name='enroll_course'),
    path('courses/<int:course_id>', login_required(StudentListMarkView.as_view()), name='student_list_mark'),
    path('courses/update_mark/<int:mark_id>', login_required(UpdateMarkView.as_view()), name='update_mark'),
    path('evolution/<int:course_id>/', login_required(evolution), name='evolution'),
    
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
  

]
