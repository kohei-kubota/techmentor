from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tinymce.models import HTMLField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    avatar = models.FileField(upload_to='avatar')
    photo = models.FileField(upload_to='profile', blank=True)
    email = models.EmailField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.user.username


class Mentor(models.Model):
    name = models.CharField(max_length=500)
    specialty = models.TextField()
    skill = models.ManyToManyField('Skill', through="Skill_Detail")
    about = models.TextField()
    description = models.TextField()
    performance = HTMLField()
    job = models.CharField(max_length=100, default="エンジニア")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    mentor_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=50)
    icon = models.FileField(upload_to='skills')
    link = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Skill_Detail(models.Model):
    mentor = models.ForeignKey('Mentor', related_name="mentor_info")
    skill = models.ForeignKey('Skill', related_name="skill_list")
    detail = models.TextField()
    experience = models.IntegerField(default=3)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.detail

class Available(models.Model):
    mentor = models.ForeignKey(Mentor)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    status = models.BooleanField(default=False)


class Review(models.Model):
    mentor = models.ForeignKey(Mentor)
    user = models.ForeignKey(User)
    content = models.TextField()

    def __str__(self):
        return self.content

class Reserve(models.Model):
    user = models.ForeignKey(User)
    mentor = models.ForeignKey(Mentor)
    date_time = models.DateTimeField(auto_now=False)


class Infomation(models.Model):
    title = models.CharField(max_length=200)
    description = HTMLField()
    tag = models.CharField(max_length=100)
    date_time = models.DateTimeField(default=timezone.now)

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=100)
    text = models.TextField()




