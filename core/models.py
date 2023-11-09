from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    STATUS_CHOICES = (
        ('I', 'Inscripciones'),
        ('P', 'En progreso'),
        ('F', 'Finalizado'),
    )
    name = models.CharField(max_length=90, verbose_name='Nombre')
    description = models.TextField(blank=True, null=True, verbose_name='Descripción')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'profesores'}, verbose_name='Profesor')
    class_quantity = models.PositiveIntegerField(default=0, verbose_name='Cantidad de clases')
    schedule = models.CharField(max_length=11, verbose_name='Horario (HH:MM-HH:MM)')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Costo', default=0.00)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='I', verbose_name='Estado')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

#Inscripciones

class Registration(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students_registration', limit_choices_to={'groups__name': 'estudiantes'}, verbose_name='Estudiante')


    def __str__(self):
        return f'{self.student.username} - {self.course.name}'

    class Meta:
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'

# NOTAS
class Mark(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso')
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'estudiantes'}, verbose_name='Estudiante')
    mark_1 = models.PositiveIntegerField(null=True, blank=True, verbose_name='Nota 1')
    mark_2 = models.PositiveIntegerField(null=True, blank=True, verbose_name='Nota 2')
    mark_3 = models.PositiveIntegerField(null=True, blank=True, verbose_name='Nota 3')
    average = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, verbose_name='Promedio')

    def __str__(self):
        return str(self.course)

    # Calcular el promedio (llamo a una función)
    def calculate_average(self):
        marks = [self.mark_1, self.mark_2, self.mark_3]
        valid_marks = [mark for mark in marks if mark is not None]
        if valid_marks:
            return sum(valid_marks) / len(valid_marks)
        return None

    def save(self, *args, **kwargs):
        # Verifico si alguna nota cambio
        if self.mark_1 or self.mark_2 or self.mark_3:
            self.average = self.calculate_average()     # Calcular el promedio (llamo a una función)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'

    
