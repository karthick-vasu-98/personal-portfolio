from django.db import models
from datetime import datetime
from . import app_gv as gv
from django.contrib.auth.models import User


class SkillCategory(models.Model):
    category_id = models.CharField(max_length=255, null=False, blank=False, unique=True, db_index=True)
    category_name = models.CharField(max_length=255, null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=12, null=True, blank=True, choices=gv.DATAMODE, default='A')

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        if not(self.category_id):
            self.category_id = 'category-'+'%02d'%(self.id)

    def __self__(self):
        return "{0}-{1}".format(self.category_id, self.category_name)
    
    class Meta:
        db_table = 'skill_category'


class Profile(models.Model):
    profile_id = models.CharField(max_length=255, null=False, blank=False, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    designation = models.CharField(max_length=255, null=True, blank=True)
    mobile_number = models.CharField(max_length=10, blank=False, null=False)
    email = models.EmailField(null=False, blank=False)
    linkedin_url = models.URLField(null=False, blank=False)
    github_url = models.URLField(null=True, blank=True)
    personal_website_url = models.URLField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    profile_summary = models.TextField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=12, null=True, blank=True, choices=gv.DATAMODE, default='A')
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        if not(self.profile_id):
            self.profile_id = 'profile-'+'%04d'%(self.id)

    def __self__(self):
        return "{0}-{1}".format(self.first_name, self.last_name)
    
    class Meta:
        db_table = 'profile_summary'


class ProfileSkills(models.Model):
    skill_category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE)
    profile = models.CharField(max_length=255, null=False, blank=False)
    skill_name = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=12, null=True, blank=True, choices=gv.DATAMODE, default='A')

    def __self__(self):
        return "{0}-{1}".format(self.profile, self.skill_name)
    
    class Meta:
        db_table = 'profile_skill'


class ProfileEducation(models.Model):
    profile = models.CharField(max_length=255, null=False, blank=False)
    degree = models.CharField(max_length=255, null=False, blank=False)
    institute_name = models.CharField(max_length=255, null=False, blank=False)
    joining_year = models.IntegerField(null=False, blank=False)
    passing_year = models.IntegerField(null=False, blank=False)
    institute_state = models.CharField(max_length=255, null=True, blank=True)
    institute_city = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=12, null=True, blank=True, choices=gv.DATAMODE, default='A')

    def __self__(self):
        return "{0}-{1}".format(self.profile, self.degree)
    
    class Meta:
        db_table = 'profile_education'


class ProfileProject(models.Model):
    profile = models.CharField(max_length=255, null=False, blank=False)
    project_name = models.CharField(max_length=255, null=True, blank=True)
    project_description = models.TextField(null=False, blank=False)
    project_skills = models.JSONField(null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=12, null=True, blank=True, choices=gv.DATAMODE, default='A')

    def __self__(self):
        return "{0}-{1}".format(self.profile, self.degree)
    
    class Meta:
        db_table = 'profile_project'



class ProfileExperience(models.Model):
    profile = models.CharField(max_length=255, null=False, blank=False)
    organization_name = models.CharField(max_length=255)
    organization_location = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=12, null=True, blank=True, choices=gv.DATAMODE, default='A')

    def __self__(self):
        return "{0}-{1}".format(self.profile, self.organization_name)
    
    class Meta:
        db_table = 'profile_experience'


class ExperienceDetail(models.Model):
    experience = models.ForeignKey(ProfileExperience, on_delete=models.CASCADE)
    designation_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=12, null=True, blank=True, choices=gv.DATAMODE, default='A')

    def __self__(self):
        return "{0}-({1} to {2})".format(self.designation_name, self.start_year.strftime("%B %Y"), self.end_year.strftime("%B %Y"))
    
    class Meta:
        db_table = 'experience_detail'



class ExperienceResponsibilities(models.Model):
    experience_detail = models.ForeignKey(ExperienceDetail, on_delete=models.CASCADE)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=12, null=True, blank=True, choices=gv.DATAMODE, default='A')

    def __self__(self):
        return "{0}".format(self.experience_detail.designation_name)
    
    class Meta:
        db_table = 'experience_responsibilities'


class CreatedResume(models.Model):
    profile = models.CharField(max_length=255, null=False, blank=False)
    resume = models.URLField(null=True, blank=True)
    resume_count = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=12, null=True, blank=True, choices=gv.DATAMODE, default='A')

    def __self__(self):
        return "{0}".format(self.profile)
    
    class Meta:
        db_table = 'created_resume'


