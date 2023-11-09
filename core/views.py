from typing import Any
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group
from django.views import View
from .forms import RegisterForm, UserForm, ProfileForm, CourseForm
from django.contrib.auth import authenticate, login
from .models import Course, Registration, Mark
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import JsonResponse
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from openpyxl import Workbook

#  Create your views here.

def plural_to_singular(plural):
    # Diccionario de palabras
    plural_singular = {
        "estudiantes": "estudiante",
        "profesores": "profesor",
        "preceptores": "preceptor",
        "administrativos": "administrativo",
    }

    return plural_singular.get(plural, "error")

def add_group_name_to_context(view_class):
    orginal_dispatch = view_class.dispatch

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        group = user.groups.first()
        group_name = None
        group_name_singular = None
        if group:
                group_name = group.name
                group_name_singular = plural_to_singular(group.name)

        context={
        'group_name': group_name,
        'group_name_singular': group_name_singular
        } 

        self.extra_context = context
        return orginal_dispatch(self, request, *args, **kwargs)

    view_class.dispatch = dispatch
    return view_class

     

#pagina inicio
@add_group_name_to_context
class HomeView(TemplateView):
    template_name='home.html'

#registrousuario
class RegisterView(View):
    def get(self, request):
        data = {
            'form': RegisterForm()
        }
        return render(request, 'registration/register.html', data)

    def post(self, request):
        user_creation_form = RegisterForm(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            user = authenticate(username=user_creation_form.cleaned_data['username'],
                                password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('home')
        data = {
            'form': user_creation_form
        }
        return render(request, 'registration/register.html', data)

# Pagina del perfil
@add_group_name_to_context
class ProfileView(TemplateView):
    template_name = 'profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_form'] = UserForm(instance=user)
        context['profile_form'] = ProfileForm(instance=user.profile)

        if user.groups.first().name == 'profesores':
            # cursos asignados al profesor
            assigned_courses = Course.objects.filter(teacher=user)
            context['assigned_courses'] = assigned_courses

        elif user.groups.first().name == 'estudiantes':
            regristrations = Registration.objects.filter(student=user) 
            enrolled_courses = [registration.course for registration in regristrations ]
            context['enrolled_courses'] = enrolled_courses

        
        return context    
    
    def post(self, request,*args,**kwargs):
        user = self.request.user
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            #Redireccion pagina de perfil (datos actualizados) 

            return redirect('profile')
        
        #Por si un dato no es valido 
        context = self.get_context_data()
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        return render(request, 'profile/profile.html', context)
    
#Mostrar cursos
@add_group_name_to_context
class CoursesView(TemplateView):
    template_name = 'courses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = Course.objects.all().order_by('-id')
        student = self.request.user if self.request.user.is_authenticated else None

        for item in courses:
            if student:
                registration = Registration.objects.filter(course=item, student=student).first()
                item.is_enrolled = registration is not None
            else:
                item.is_enrolled = False

            enrollment_count = Registration.objects.filter(course=item).count()
            item.enrollment_count = enrollment_count

        context['courses'] = courses
        return context
      
#crear nuevos cursos
@add_group_name_to_context
class CourseCreateView(UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm 
    template_name = 'create_course.html'
    success_url = reverse_lazy('courses')
# pagina permisos
    def test_func(self):
        return self.request.user.groups.filter(name='administrativos').exists()

#registro curso
    def form_valid(self, form):
        messages.success(self.request, 'El registro se guardo correctamente')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'El registro no se guardo correctamente')
        return self.render_to_response(self.get_context_data(form=form))

@add_group_name_to_context
class  CourseEditView(UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'edit_course.html'
    success_url = reverse_lazy('courses')  

    def test_func(self):
        return self.request.user.groups.filter(name='administrativos').exists()
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'El registro se ha actualizado correctamente')
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        messages.error(self.request, 'El registro no se guardo correctamente')
        return self.render_to_response(self.get_context_data(form=form))
    

@add_group_name_to_context
class CourseDeleteView(UserPassesTestMixin, DeleteView):
    model = Course
    template_name = 'delete_course.html'
    success_url = reverse_lazy('courses')

    def test_func(self):
        return self.request.user.groups.filter(name='administrativos').exists()

    def form_valid(self, form):
        messages.success(self.request, 'El registro se ha eliminado correctamente')
        return super().form_valid(form)

#Registro Usuarios1
@add_group_name_to_context
class CourseEnrollmentView(TemplateView):
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        if request.user.is_authenticated and request.user.groups.first().name == 'estudiantes':
            student = request.user

            # Crear un registro de inscripción asociado al estudiante y el curso
            registration = Registration(course=course, student=student)
            registration.save()

            # Enviar correo de verificación
            subject = 'Verificación de inscripción en el curso'
            message = '¡Gracias por inscribirte en el curso! Tu inscripción ha sido verificada.'
            from_email = 'jelxdjango@gmail.com'  # El remitente del correo
            recipient_list = [student.email]  # La dirección de correo del estudiante

            send_mail(subject, message, from_email, recipient_list)

            messages.success(request, 'Inscripción exitosa y correo de verificación enviado')
        else:
            messages.error(request, 'No se pudo completar la inscripción')

        return redirect('courses')
    
#Registro Usuarios
@add_group_name_to_context
class StudentListMarkView(TemplateView):
    template_name = 'student_list_mark.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs['course_id']
        course = get_object_or_404(Course, id=course_id)
        marks = Mark.objects.filter(course=course)

        student_data = []
        for mark in marks:
            student = get_object_or_404(User, id=mark.student_id)
            student_data.append({
                'mark_id': mark.id,
                'name': student.get_full_name(),
                'mark_1': mark.mark_1,
                'mark_2': mark.mark_2,
                'mark_3': mark.mark_3,
                'average': mark.average,
            })
        
        context['course'] = course
        context['student_data'] = student_data
        return context
    
#agregar notas    
@add_group_name_to_context
class UpdateMarkView(UpdateView):
    model = Mark
    fields = ['mark_1', 'mark_2', 'mark_3']
    template_name = 'update_mark.html'

    def get_success_url(self):
        return reverse_lazy('student_list_mark', kwargs={'course_id': self.object.course.id})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mark = self.get_object()
        context ['course_name'] = mark.course.name 
        return context
    
    def get_object(self, queryset=None):
        mark_id = self.kwargs['mark_id']
        return get_object_or_404(Mark, id=mark_id)
      
    
from django.shortcuts import render

def evolution(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    teacher = course.teacher.get_full_name()
    class_quantity = course.class_quantity
    student = request.user

    # Obtengo las notas
    marks = Mark.objects.filter(course=course, student=student)

    context = {
        'teacher': teacher,
        'class_quantity': class_quantity,
        'courseName': course.name,
        'marks': marks
    }

    return render(request, 'evolution.html', context)

