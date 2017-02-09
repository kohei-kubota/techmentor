from django import forms
from django.forms import ModelForm
from .models import Mentor, Profile, Skill_Detail, Reserve, Available, Contact
from tinymce.widgets import TinyMCE

class MentorForm(ModelForm):
    class Meta:
        model = Mentor
        fields = ['name', 'specialty', 'about', 'description', 'performance', 'status']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'photo', 'email']

class SkillForm(ModelForm):
    class Meta:
        model = Skill_Detail
        fields = ['detail', 'experience', 'status']

class AddSkillForm(ModelForm):
    class Meta:
        model = Skill_Detail
        fields = ['skill', 'detail', 'experience', 'status']


class SomeForm(forms.Form):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

class ReserveForm(ModelForm):
    class Meta:
        model = Reserve
        fields = ['date_time']

class ScheduleForm(ModelForm):
    class Meta:
        model = Available
        fields = ['date', 'time', 'status']

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'text']