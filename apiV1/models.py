from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    start_date = models.DateTimeField()
    cost = models.DecimalField(max_digits=16, decimal_places=2)


class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    video_link = models.URLField()


class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    name = models.CharField(max_length=32)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=False, blank=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    min_users = models.PositiveSmallIntegerField()
    max_users = models.PositiveSmallIntegerField()
    students = models.ManyToManyField(Student, related_name='groups')


class UserProductAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')
