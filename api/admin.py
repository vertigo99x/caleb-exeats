from django.contrib import admin

from .models import Allusers, College, Student, Events, Forms, Descriptions, Hostels, Departments

admin.site.register(Allusers)
admin.site.register(Student)
admin.site.register(Events)
admin.site.register(Forms) 
admin.site.register(Hostels) 
admin.site.register(Departments) 
admin.site.register(College) 
admin.site.register(Descriptions) 
