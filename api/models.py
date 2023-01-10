from email.policy import default
from django.db import models

from django.core.files import File

from io import BytesIO

from PIL import Image

from datetime import datetime
from django.conf import settings


class Allusers(models.Model):

    usercatChoices = [('',''),('student','student'),('porter','porter'),('parent','parent'),('saffairs','saffairs'),('security','security'),('superuser','superuser')]
    genderchoices = [('',''),('male','male'),('female','female')]
    formsleft_choices = [('',''),(0,0),(1,1),(2,2)] 
    
    username = models.CharField(null=False, blank=False, max_length=255)
    usercat = models.CharField(null=False, blank=False, max_length=255, choices=usercatChoices)
    gender = models.CharField(null=False, blank=False, max_length=255, choices=genderchoices)
    firstname = models.CharField(null=False, blank=False, max_length=255)
    middlename = models.CharField(null=True, blank=True, max_length=255)
    lastname = models.CharField(null=False, blank=False, max_length=255)
    phonenumber = models.CharField(null=False, blank=False, max_length=255)
    alternate_number = models.CharField(null=True, blank=True, max_length=255)
    
    hostel = models.CharField(null=False, blank=False, max_length=255,default='none')
    email = models.CharField(null=False, blank=False, max_length=255, default='')
    pendingexeats = models.CharField(null=False, blank=False, max_length=255, default='0')
    approvedexeats = models.CharField(null=False, blank=False, max_length=255, default='0')
    rejectedexeats = models.CharField(null=False, blank=False, max_length=255, default='0')
    
    image = models.ImageField(upload_to=f'uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/',blank=True, null=True)
    is_default_pass = models.BooleanField(default=True)
    
    forms_left = models.CharField(null=False, blank=False, max_length=255, default='2')
    last_form_sent_day = models.CharField(null=True, blank=True, max_length=255, default='')
    
    date_added_main = models.CharField(null=True, blank=True, max_length=255, default='')
    home_address = models.CharField(
        null=False, blank=False, max_length=255, default='None')

    date_added = models.DateTimeField(auto_now = True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-date_added']
        
    def __str__(self):
        return self.username
    
    def get_image(self):
        if self.image:
            return settings.MAINMEDIANAME + self.image.url
        return ''
    
    
class Student(models.Model):   
    colleges = [('',''),('COPAS','C.O.P.A.S.'),('CASMAS','C.A.S.M.A.S.'),('COLENSMAS','C.O.L.E.N.S.M.A.S')]
    home_address = models.CharField(null=False, blank=False, max_length=255)
    parent_phone_no = models.CharField(null=False, blank=False, max_length=255)
    alternate_parent_phone_no = models.CharField(null=True, blank=True, max_length=255)
    parent_email = models.CharField(null=False, blank=False, max_length=255)
    student_level = models.CharField(null=False, blank=False, max_length=255)
    gender = models.CharField(null=False, blank=False, max_length=255)
    matric_no = models.CharField(primary_key=True, null=False, blank=False, max_length=255)
    department= models.CharField(null=False, blank=False, max_length=255, default='')
    college = models.CharField(null=False, blank=False, max_length=255, default='',choices=colleges)
   
    
     
    class Meta:
        ordering = ['student_level']
        
    def __str__(self):
        return self.matric_no
    

class Forms(models.Model):
    choices = [('',''),('0','0'),('1','1'),('2','2')]
    levels = [('',''),('100','100'),('200','200'),('300','300'),('400','400')]
    colleges = [('',''),('COPAS','C.O.P.A.S.'),('CASMAS','C.A.S.M.A.S.'),('COLENSMAS','C.O.L.E.N.S.M.A.S')]
    
    matric_no = models.CharField(null=False, blank=False, max_length=255)
    level = models.CharField(null=False, blank=False, max_length=255, choices=levels, default='')
    fullname = models.CharField(null=False, blank=False, max_length=255)
    studentpic = models.CharField(null=True, blank=True, max_length=625)
    exeat_type = models.CharField(null=False, blank=False, max_length=255)
    exeat_description = models.CharField(null=False, blank=False, max_length=255)
    departure_date = models.CharField(null=False, blank=False, max_length=255)
    arrival_date = models.CharField(null=False, blank=False, max_length=255)
    hostel = models.CharField(null=False, blank=False, max_length=255)
    parent_no = models.CharField(null=True, blank=True, max_length=255)
    parentemail = models.CharField(null=True, blank=True, max_length=255)
    students_no = models.CharField(null=True, blank=True, max_length=255)
    statusPorter = models.CharField(null=False, blank=False, max_length=255, default='0', choices=choices)
    statusParent = models.CharField(null=False, blank=False, max_length=255, default='0',choices=choices)
    statusStudentAffairs = models.CharField(null=False, blank=False, max_length=255, default='0', choices=choices)
    iscancelled = models.BooleanField(default=False)
    department = models.CharField(null=False, blank=False, max_length=255, default='')
    college = models.CharField(null=False, blank=False, max_length=255, default='',choices=colleges)
    date_added_main = models.CharField(null=False, blank=False, max_length=255, default = '')
    
    date_added = models.DateTimeField(auto_now_add = True)
    
    
    class Meta:
        ordering = ['-date_added']
        
    def __str__(self):
        return f"CUEXT{self.id} -> {self.matric_no} -> {self.exeat_description}"

class Events(models.Model):
    choices = [('primary','primary'),('danger','danger'),('success','success')]
    username = models.CharField(null=False, blank=False, max_length=255)
    notification = models.CharField(null=False, blank=False, max_length=255)
    receiver = models.CharField(null=False, blank=False, max_length=255)
    tag = models.CharField(null=False, blank=False, max_length=255, default='primary',choices=choices)
    date_added_main = models.CharField(null=False, blank=False, max_length=255, default = '')
    
    date_added = models.DateTimeField(auto_now_add = True)
    
    
    class Meta:
        ordering = ['-date_added']
        
        
    def __str__(self):
        return F"{self.username} -> {self.receiver} | {self.notification} | | {self.date_added}"
   
   
class Descriptions(models.Model):
    description = models.CharField(null=False, blank=False, max_length=255)
    
    def __str__(self):
        return self.description
    
class Hostels(models.Model):
    genderchoices = [('',''),('male','male'),('female','female')]
    gender=models.CharField(null=False, blank=False, max_length=255, choices=genderchoices, default = '')
    hostel_name=models.CharField(null=False, blank=False, max_length=255, default = '')
    
    def __str__(self):
        return self.hostel_name + ' hall'
    
    
class College(models.Model):
    colleges = models.CharField(null=False, blank=False, max_length=255, default = '')
    departments = models.TextField(null=False, blank=False, max_length=1000, default = '')
    
    def __str__(self):
        return self.colleges + f' [{self.departments}]'
    
class Departments(models.Model):
    college = models.CharField(null=False, blank=False, max_length=255, default = '')
    department = models.CharField(null=False, blank=False, max_length=255, default = '')
    
    def __str__(self):
        return self.department + ' -> ' + self.college
    
    
class Tickets(models.Model):
    useraname = models.CharField(null=False, blank=False, max_length=255, default = '')
    priority = models.IntegerField(null=False, blank=False, default = 3)
    complaint = models.TextField(null=False, blank=False, max_length=500, default = '')
    date_added = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f'{self.useraname} -> {self.complaint[:20]}... priority: {self.priority}'
    
'''
class Parent(models.Model):
    username = models.CharField(null=False, blank=False, max_length=255)
    students_matric_number_array = models.CharField(null=False, blank=False, max_length=255)
    students_number_array = models.CharField(null=False, blank=False, max_length=255) 
'''