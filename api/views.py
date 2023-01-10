from django.shortcuts import render, Http404

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .models import Allusers, College, Student, Events, Forms, Descriptions, Hostels, Departments

from django.db.models import Q

from .serializers import AllusersSerializer, CollegeSerializer, StudentSerializer, EventsSerializer, FormsSerializer, DescriptionsSerializer, HostelsSerializer, DepartmentsSerializer

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from django.conf import settings

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import os
from datetime import datetime

from threading import Thread

import time
import psycopg2
import random



higher_ups = ['porter', 'saffairs']

default_student_password = 'calebuniv'


def autoCancelForm(): #automatically cancels form when date is passed
    while True:
        if datetime.now().day > 2:
            forms=Forms.objects.filter(departure_date = f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day-2}").filter(Q(statusPorter='0') | Q(statusParent='0') | Q(statusStudentAffairs='0'))
            form_values = forms.values()
            for x in form_values:
                username = x['matric_no']
                
                forms.update(iscancelled=1)
                event = Events.objects.create(
                    username = username,
                    notification = f"Your Request was cancelled as the departure date has been exceeded (FormID: CULEXT{x['id']})",
                    receiver = username,
                    tag = 'danger',
                    date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
                    
                )
                event.save();
        
        time.sleep(82800)
       
gon_freecks = Thread(target=autoCancelForm, daemon=True).start()



def customTaskThread(username, sql, command, usercat, bulkFunction):
    if bulkFunction == 'customTask':
        college = sql['college']
        description = sql['description']
        level = sql['level']
        hostel = sql['hostel']
        
        data = Forms.objects.filter(hostel=hostel).filter(Q(exeat_description=description) | Q(exeat_description=description.lower()) | Q(exeat_description=description.upper()) | Q(exeat_description=description.capitalize())).filter(iscancelled = False)
        
        if level != 'all':
            data = data.filter(level=level)
        
        if college != 'all':
            data = data.filter(college=college)
        
            
        if sql['whoami'].strip().lower() == 'porter':
            data = data.filter(statusPorter = 0)
        elif sql['whoami'].strip().lower() == 'saffairs':
            data = data.filter(statusStudentAffairs = 0)
        
        
        g=[{'id':x['id'],'matric_no':x['matric_no']} for x in data.values()][::-1]
        print(g)
    
    elif bulkFunction == 'bulkTask':
        g=sql

    change = command
    taskType = bulkFunction
    
    if change.lower().strip() == "approve":
        if usercat.lower() == 'porter': 
            for x in g:
                matric_no, formpk = x['matric_no'], x['id']
                Forms.objects.filter(id=formpk).update(statusPorter = '1')
            
                event = Events.objects.create(
                    username = username,
                    notification = f"You Approved a request from {matric_no} with {taskType} (FormID: CULEXT{formpk})",
                    receiver = username,
                    tag = 'success',
                    date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
            
                )
                event.save();
                
                event = Events.objects.create(
                    username = username,
                    notification = f"Your request has been Approved by your Porter (FormID: CULEXT{formpk})",
                    receiver = matric_no,
                    tag = 'success',
                    date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
                )
                event.save();
          
 
        
        elif usercat.lower() == 'saffairs': 
            for x in g:
                matric_no, formpk = x['matric_no'], x['id']
                
                Forms.objects.filter(id=formpk).update(statusStudentAffairs = '1')
                event = Events.objects.create(
                    username = username,
                    notification = f"You Approved a request from {matric_no} with {taskType} (FormID: CULEXT{formpk})",
                    receiver = username,
                    tag = 'success',
                    date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
            
                )
                event.save();
                
                event = Events.objects.create(
                    username = username,
                    notification = f"Student Affairs has Approved your Request (FormID: CULEXT{formpk})",
                    receiver = matric_no,
                    tag = 'success',
                    date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
            
                )
                event.save();
                   
    elif change.lower().strip() == 'reject':
        if usercat.lower() == 'porter': 
            for x in g:
                matric_no, formpk = x['matric_no'], x['id']
                Forms.objects.filter(id=formpk).update(statusPorter = '2')
                event = Events.objects.create(
                    username = username,
                    notification = f"You Rejected a request from {matric_no} with {taskType} (FormID: CULEXT{formpk})",
                    receiver = username,
                    tag = 'danger',
                    date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
            
                )
                event.save();
                
                event = Events.objects.create(
                    username = username,
                    notification = f"Your request has been Rejected by your Porter (FormID: CULEXT{formpk})",
                    receiver = matric_no,
                    tag = 'danger',
                    date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
            
                )
                event.save();
   
        elif usercat.lower() == 'saffairs': 
            for x in g:
                matric_no, formpk = x['matric_no'], x['id']
                Forms.objects.filter(id=formpk).update(statusStudentAffairs ='2')
                event = Events.objects.create(
                    username = username,
                    notification = f"You Rejected a request from {matric_no} with {taskType} (FormID: CULEXT{formpk})",
                    receiver = username,
                    tag = 'danger',
                    date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
            
                )
                event.save();
                
                event = Events.objects.create(
                    username = username,
                    notification = f"Student Affairs Rejected your request (FormID: CULEXT{formpk})",
                    receiver = matric_no,
                    tag = 'danger',
                    date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
            
                )
                event.save();
            
        
def bulkRegistration(csvLink):
    
    with open(fr'{settings.MEDIA_ROOT}\docs\bulk_docs\{csvLink}') as handler:
        handle = open(fr'{settings.MEDIA_ROOT}/docs/logs.txt','w')
        handle = open(fr'{settings.MEDIA_ROOT}/docs/logs.txt','r+')
        
        password = default_student_password
        main = handler.readlines()
        if len(main[0].split(',')) == 15:
            for x, y in enumerate(main[1:]):
                email, matric_no,gender,fullname,hostel,student_level,college,department,address,phone_no, alt_phone_no,parent_email,parent_phone_no,alternate_parent_phone_no,p_name = y.split(',')
                
                name = fullname.split(' ')
                matric_no = matric_no.replace('/', '-')
                
                if len(name)==3:
                    lastname, firstname, middlename = name
                    
                elif len(name)==2:
                    lastname, firstname == name
                    middlename= ''
                else:
                    lastname, firstname, middlename = name, ' ', ' '  
                
                if email == '' or matric_no == '' or gender == '' or fullname == '' or hostel == '' or student_level == '' or college == '' or department == '' or phone_no =='' or parent_email == '' or parent_phone_no =='' or p_name == '':
                    handle.writelines(f"{x+1}|{email}, {matric_no} --> Incomplete info \n")
                    handle.flush()
                else:
                    user = User.objects.filter(Q(username=matric_no) | Q(email=email))
                    if (len(user)) == 0:
                        allusers = Allusers.objects.filter(Q(username=matric_no) | Q(email=email))
                        students = Student.objects.filter(matric_no=matric_no)
                        if len(allusers) == 0:
                            if len(students) == 0:
                                user = User.objects.create_user(username=matric_no, email=email, password=password)
                                user.save()
                                user = Allusers.objects.create(
                                    username=matric_no,
                                    usercat='student',
                                    gender=gender,
                                    firstname=firstname,
                                    lastname=lastname,
                                    middlename=middlename,
                                    phonenumber=phone_no,
                                    alternate_number=alt_phone_no,
                                    hostel=hostel,
                                    email=email,
                                    home_address=address,
                                    image = f'{settings.MEDIA_ROOT}/profile.png',
                                    forms_left=2,
                                )
                                user.save()

                                user = Student.objects.create(
                                    home_address=address,
                                    parent_phone_no=parent_phone_no,
                                    alternate_parent_phone_no=alternate_parent_phone_no,
                                    parent_email=parent_email,
                                    student_level=student_level,
                                    gender=gender,
                                    department=department,
                                    matric_no=matric_no,
                                    college=college,
                                )
                                user.save()

                                event = Events.objects.create(
                                    username=matric_no,
                                    notification=f"Welcome to Caleb Exeats {firstname}",
                                    receiver=matric_no,
                                    tag='success',
                                    date_added_main=f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"

                                )

                                event.save()
                                
                                event = Events.objects.create(
                                    username='admin',
                                    notification=f"You Registered {matric_no}",
                                    receiver='admin',
                                    tag='success',
                                    date_added_main=f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"

                                )

                                event.save()

                                is_reg_student = True

                                parent_check = Allusers.objects.filter(
                                    username=parent_email)
                                parent_phone_check = Student.objects.filter(
                                    parent_phone_no=parent_email)
                                parent_phone_alt_check = Student.objects.filter(
                                    alternate_parent_phone_no=parent_email)
                                parent_check_user = User.objects.filter(
                                    username=parent_email)
                                if len(parent_check) == 0 and len(parent_check_user) == 0 and len(parent_phone_check) == 0 and len(parent_phone_alt_check) == 0:
                                    user = User.objects.create_user(
                                        username=parent_email, email=parent_email, password=password)
                                    user.save()

                                    parent_name = p_name.split('|')
                                    if len(parent_name) == 2:
                                        firstname, lastname = parent_name
                                        middlename = ' '
                                    elif len(parent_name) == 3:
                                        firstname, middlename, lastname = parent_name
                                    else:
                                        lastname, firstname, middlename = fullname, ' ', ' '

                                    user = Allusers.objects.create(
                                        username=parent_email,
                                        usercat='parent',
                                        gender=gender,
                                        firstname=firstname,
                                        lastname=lastname,
                                        middlename=middlename,
                                        phonenumber=parent_phone_no,
                                        alternate_number=alternate_parent_phone_no,
                                        hostel='none',
                                        email=parent_email,
                                        image=f'{settings.MEDIA_ROOT}/profile.png',
                                    )
                                    user.save()

                                    event = Events.objects.create(
                                        username=matric_no,
                                        notification=f"Welcome to Caleb Exeats.",
                                        receiver=parent_email,
                                        tag='success',
                                        date_added_main=f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"

                                    )

                                    event.save()
                                    
                                    event = Events.objects.create(
                                        username='admin',
                                        notification=f"You Registered {parent_email}",
                                        receiver='admin',
                                        tag='success',
                                        date_added_main=f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"

                                    )

                                    event.save()

                                    is_reg_parent = True

                                else:
                                    handle.writelines(f"{x+1}|{email}, {matric_no} --> Parent Already Exists (skipped) \n")
                                    handle.flush()

                            else:
                                handle.writelines(
                                    f"{x+1}|{email}, {matric_no} --> matric No. Already Exists in Students DB \n")
                                handle.flush()

                        else:
                            handle.writelines(
                                f"{x+1}|{email}, {matric_no} --> Username or email Already Exists in AllUsers DB \n")
                            handle.flush()

                    else:
                        handle.writelines(
                            f"{x+1}|{email}, {matric_no} --> User Already Exists in General User DB \n")
                        handle.flush()
                        
            handle.close()
            
    os.remove(fr'{settings.MEDIA_ROOT}\docs\bulk_docs\{csvLink}')
   
   
   
class BulkTask(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        token = data['token'].strip()
        command = data['command'].lower().strip()
        password = data['password']
        pk_array = data['pk_list']
        
        is_token = Token.objects.filter(key=token).values()[0]
        user = User.objects.filter(id=is_token['user_id'])
        username = user.values()[0]['username']
        
        all_u = Allusers.objects.filter(username=username).values()[0]
        usercat = all_u['usercat'].lower()
        hostel = all_u['hostel'].strip().lower()
        
        if usercat != 'porter' and usercat !='saffairs':
            return Response({'message':'unauthorized_user'})
        if command != 'approve' and command != 'reject':
            return Response({'message':'invalid_command'})
        
        userPassword = user.values()[0]['password']
        matchcheck = check_password(password, userPassword)
        
        if matchcheck:
            startTask = Thread(target=customTaskThread, args=(username, pk_array, command, usercat, 'bulkTask'), daemon=True).start()
            
            return Response({'message':'completed_successfully'}) 
            
        return Response({'message':'incorrect_password'}) 
                

class CustomTask(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        
        token = data['token'].strip()
        username = data['username'].strip()
        password = data['password']
        college = data['college'].strip()
        command = data['command'].lower().strip()
        level = data['level'].strip()
        description = data['description'].strip()
        
        
        all_u = Allusers.objects.filter(username=username).values()[0]
        usercat = all_u['usercat'].lower()
        hostel = all_u['hostel'].strip().lower()
        is_token = Token.objects.filter(key=token).values()[0]
        user = User.objects.filter(id=is_token['user_id']).values()[0]['username']
        
        if usercat != 'porter' and usercat !='saffairs':
            return Response({'message':'unauthorized_user'})
            
        if user == username:
            user = User.objects.filter(username=username)
            userPassword = user.values()[0]['password']
            matchcheck = check_password(password, userPassword)
            
            if matchcheck:
                
                if command.strip() == 'approve':
                    switchStat = 1
                elif command.strip() == 'reject':
                    SwitchStat = 2
                else:
                    return Response({'message':'invalid_command'})
                
                sql = {}
                  
                if usercat == 'porter':
                    #sql = f"""SELECT * from api_forms where {type1} {type2} {type3} and hostel='{hostel}' and statusPorter='0' """
                    
                    sql['hostel'] = hostel
                    sql['college'] = college
                    sql['level'] = level
                    sql['description'] = description
                    sql['whoami'] = 'porter'
                    
                    
                if usercat == 'saffaris':
                    #sql = f"""SELECT * from api_forms where {type1} {type2} {type3} and statusStudentAffairs='0' """
                    sql['hostel'] = hostel
                    sql['college'] = college
                    sql['level'] = level
                    sql['description'] = description
                    sql['whoami'] = 'porter'
            
                
            
                startTask = Thread(target=customTaskThread, args=(username, sql, command, usercat, 'customTask'), daemon=True).start()
               
                return Response({'message':'completed_successfully'}) 
            
            return Response({'message':'incorrect_password'}) 
         
        return Response({'message':'unauthorized_user'})  



 
class GetDescriptions(APIView):
    def get(self, request, format=None):
        desc = Descriptions.objects.all()
        serializer = DescriptionsSerializer(desc, many=True)
        return Response(serializer.data)
    
    
    
class GetColleges(APIView):
    def get(self, request, format=None):
        desc = College.objects.all()
        serializer = CollegeSerializer(desc, many=True)
        return Response(serializer.data)
    


class ProfileDetails(APIView):
    def get(self, request,username, format=None):
        user = Allusers.objects.filter(username=username).values()[0]
        student_data = Student.objects.filter(matric_no=username).all().values()
        data = {
            'level':student_data[0]['student_level'],
            'homeAddress':student_data[0]['home_address'],
            'college':student_data[0]['college']
        }
        
        return Response(data)
    
        


class ChangePassword(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        
        username = data['username']
        token = data['token']
        old_password = data['old_password']
        new_password = data['new_password']
        
        is_token = Token.objects.filter(key=token).values()[0]
        user = User.objects.filter(id=is_token['user_id']).values()[0]['username']
        
        if user == username:
            user = User.objects.filter(username=username)
            userPassword = user.values()[0]['password']
            matchcheck = check_password(old_password, userPassword)
            u = user[0]
            if matchcheck:
                u.set_password(new_password)
                u.save()
                
                return Response({'message':'success'})
            
            return Response({'message':'incorrect_old_password'})
        
        return Response({'message':'incorrect_auth_details'})


class ChangeProfileImage(APIView):
    def post(self, request, *args, **kwargs):
        valid_extensions = ['jpg','png','jpeg']
        g=request.data     
        print(g)   
        duc = g['formdata']
        token = g['token']
        document_text = str(duc)
        if document_text.split('.')[-1] not in valid_extensions:
            return Response({'message':'invalid extension'})
        
        is_token = Token.objects.filter(key=token).values()[0]
        username = User.objects.filter(id=is_token['user_id']).values()[0]['username']
        
        imagename = username.replace('@','-')
        allusers = Allusers.objects.filter(username=username).values()[0]
        previous_image = allusers['image']
        usercat = allusers['usercat']
        has_previous_image = False
        if previous_image.strip() != '':
            has_previous_image = True
            previous_image_path = fr"{settings.MEDIA_ROOT}\{previous_image}"
            print('previous image path: ', previous_image_path) 
            
        path = default_storage.save(fr"{settings.MEDIA_ROOT}/uploads/{username}/{document_text}", ContentFile(duc.read()))
        Allusers.objects.filter(username=username).update(image=fr'uploads/{username}/{duc}')
        
        if has_previous_image:
            try:
                os.remove(previous_image_path)
            except Exception:
                pass
            
        #if usercat.lower().strip() == 'student':
        Forms.objects.filter(matric_no = username).update(studentpic = fr"{settings.MAINMEDIANAME}/uploads/{username}/{document_text}")
        print('dunzo')
        return Response({'message':'image saved successfully'})
    
    
class Logout(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            token = data['token']
            Token.objects.filter(key=token).delete()
            
            return Response({'message':'loggged out successfully'})
        except Exception:
            return Response({'message':'log out error'})

class GetHostels(APIView):
    def get(self, request, format=None):
        hostels = Hostels.objects.all()
        serializer = HostelsSerializer(hostels, many=True)
        return Response(serializer.data)

class GetDepartments(APIView):
    def get(self, request, format=None):
        depts = Departments.objects.all()
        serializer = DepartmentsSerializer(depts, many=True)
        return Response(serializer.data)


#==============================ADMIN====================================
class GetUsersData(APIView):
    def get(self, request, token, format=None):
        is_token = Token.objects.filter(key=token).values()[0]
        user = User.objects.filter(id=is_token['user_id']).values()[0]
        is_superuser = user['is_superuser']
        is_staff = user['is_staff']
        username = user['username']
        print('hello')
        if is_staff and is_superuser:
            students = Allusers.objects.filter(usercat='student').filter(is_active=True)
            parents = Allusers.objects.filter(usercat='parent').filter(is_active=True)
            staff = Allusers.objects.filter(Q(usercat='security') | Q(usercat='porter') | Q(usercat='saffairs')).filter(is_active=True)
        
            staffCount = len(staff.values())
            studentCount = len(students.values())
            parentCount = len(parents.values())
            
            return Response({
                 'staffCount':staffCount,
                 'studentCount':studentCount,
                 'parentCount':parentCount,
                 'staff':staff.values(),
                 'parents':parents.values(),
                 'students':students.values()
                             })
            
class RegLogs(APIView):
    def get(self, request,token,format=None):
        is_token = Token.objects.filter(key=token).values()[0]
        user = User.objects.filter(id=is_token['user_id'])
        if user.values()[0]['is_superuser'] and user.values()[0]['is_staff']:
            with open(fr'{settings.MEDIA_ROOT}\docs\logs.txt','r+') as handler:
                return Response({'logs':handler.readlines()})
        return Response({'message':'unAuthorized'})
            
class RegisterStudentBulk(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data 
        duc = data['formdata']
        token = data['token']
        password = data['password']

        document_text = str(duc)
        if document_text.split('.')[-1] != 'csv':
            return Response({'message': 'File Must be a .CSV File'})

        is_token = Token.objects.filter(key=token).values()[0]
        user = User.objects.filter(id=is_token['user_id'])
        userPassword = user.values()[0]['password']
        matchcheck = check_password(password, userPassword)
        u = user[0]
        if matchcheck:    
            path = default_storage.save(fr"{settings.MEDIA_ROOT}/docs/bulk_docs/{document_text}", ContentFile(duc.read()))
            print(document_text)
            startBulkReg = Thread(target=lambda:bulkRegistration(str(document_text)), daemon=True).start()
            event = Events.objects.create(
                username='admin',
                notification=f"You Executed a Bulk Registration",
                receiver='admin',
                tag='success',
                date_added_main=f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"

            )

            event.save()

            return Response({'message':'Bulk Registration Running in background','code':1})
        
        return Response({'message':'Unauthorized'})
    
       
class RegisterUser(APIView):
    def post(self, request, *args, **kwargs):
        usercat_list=['student','porter','parent','saffairs','security']
        data = request.data
        print(data)
        
        token = data['token']
        
        
        is_token = Token.objects.filter(key=token).values()[0]
        user = User.objects.filter(id=is_token['user_id'])
        matchcheck = user.values()[0]['is_superuser']
        if matchcheck:
            usercat = data['usercat'].lower().strip()
            matric_no = data['matric_no'].lower().strip().replace('/', '-')
            phone_no = data['phone_number']
            fullname = data['fullname'].lower().strip()
            email = data['email'].lower().strip()
            parent_email = data['parent_email'].lower().strip()
            gender = data['gender'].lower().strip()
            student_level = data['student_level'].lower().strip()
            college = data['college'].lower().strip()
            department = data['department'].lower().strip()
            alt_phone_no = data['alt_phone_number'].lower().strip()
            parent_phone_no = data['parent_phone_number'].lower().strip()
            alternate_parent_phone_no = data['alt_parent_phone_number'].lower().strip()
            address = data['address'].lower().strip()
            p_name = data['parent_name']
            password = data['password']

            hostel = data['hostel'].lower().strip()

            t_name = fullname.split('|')
            if len(t_name) == 2:
                lastname, firstname = t_name
                middlename = ' '
            elif len(t_name) == 3:
                lastname, firstname, middlename  = t_name
            else:
                lastname, firstname, middlename = fullname, ' ', ' '

            if usercat == 'saffairs':
                hostel = 'none'

            # strict check

            if usercat in usercat_list and usercat != 'student':
                user = User.objects.filter(username=email)
                checked_email = User.objects.filter(email=email)
                if (len(user)) == 0 and len(checked_email) == 0:
                    user = User.objects.create_user(username=email, email=email, password=password)
                    user.save()

                    allusers = Allusers.objects.filter(username=email)
                    checked_email = Allusers.objects.filter(email=email)
                    if len(allusers) == 0 and len(checked_email) == 0:
                        user = Allusers.objects.create(
                            username=email,
                            usercat=usercat,
                            gender=gender,
                            firstname=firstname,
                            lastname=lastname,
                            middlename=middlename,
                            phonenumber=phone_no,
                            alternate_number=alt_phone_no,
                            hostel=hostel,
                            email=email,
                            home_address=address,
                            image=f'{settings.MEDIA_ROOT}/profile.png',
                        )
                        user.save()
                        
                        event = Events.objects.create(
                                        username='admin',
                                        notification=f"You Registered {email}",
                                        receiver='admin',
                                        tag='success',
                                        date_added_main=f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"

                                    )

                        event.save()


                        
                        
                        event = Events.objects.create(
                            username=email,
                            notification=f"Welcome to Caleb Exeats",
                            receiver=email,
                            tag='success',
                            date_added_main=f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"

                        )

                        event.save()

                        return Response({"message": "user created successfully"})

                    return Response({"message": "user already exists in general database"})

                return Response({"message": "user already exists in user database"})

            elif usercat == 'student':
                user = User.objects.filter(username=matric_no)
                if (len(user)) == 0:
                    allusers = Allusers.objects.filter(username=email)
                    students = Student.objects.filter(matric_no=matric_no)
                    if len(allusers) == 0:
                        if len(students) == 0:
                            user = User.objects.create_user(username=matric_no, email=email, password=password)
                            user.save()
                            user = Allusers.objects.create(
                                username=matric_no,
                                usercat='student',
                                gender=gender,
                                firstname=firstname,
                                lastname=lastname,
                                middlename=middlename,
                                phonenumber=phone_no,
                                alternate_number=alt_phone_no,
                                hostel=hostel,
                                email=email,
                                home_address=address,
                                image=f'{settings.MEDIA_ROOT}/profile.png',
                                forms_left=2,
                            )
                            user.save()

                            user = Student.objects.create(
                                home_address=address,
                                parent_phone_no=parent_phone_no,
                                alternate_parent_phone_no=alternate_parent_phone_no,
                                parent_email=parent_email,
                                student_level=student_level,
                                gender=gender,
                                department=department,
                                matric_no=matric_no,
                                college=college,
                            )
                            user.save()

                            event = Events.objects.create(
                                username=matric_no,
                                notification=f"Welcome to Caleb Exeats {firstname}",
                                receiver=matric_no,
                                tag='success',
                                date_added_main=f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"

                            )

                            event.save()
                            event = Events.objects.create(
                                        username='admin',
                                        notification=f"You Registered {matric_no}",
                                        receiver='admin',
                                        tag='success',
                                        date_added_main=f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"

                                    )

                            event.save()

                            is_reg_student = True

                            parent_check = Allusers.objects.filter(
                                username=parent_email)
                            parent_phone_check = Student.objects.filter(
                                parent_phone_no=parent_email)
                            parent_phone_alt_check = Student.objects.filter(
                                alternate_parent_phone_no=parent_email)
                            parent_check_user = User.objects.filter(
                                username=parent_email)
                            if len(parent_check) == 0 and len(parent_check_user) == 0 and len(parent_phone_check) == 0 and len(parent_phone_alt_check) == 0:
                                user = User.objects.create_user(
                                    username=parent_email, email=parent_email, password=password)
                                user.save()

                                parent_name = p_name.split('|')
                                if len(parent_name) == 2:
                                    plastname, pfirstname = parent_name
                                    pmiddlename = ' '
                                elif len(parent_name) == 3:
                                    plastname, pfirstname, pmiddlename = parent_name
                                else:
                                    plastname, pfirstname, pmiddlename = p_name, ' ', ' '

                                user = Allusers.objects.create(
                                    username=parent_email,
                                    usercat='parent',
                                    gender=gender,
                                    firstname=pfirstname,
                                    lastname=plastname,
                                    middlename=pmiddlename,
                                    phonenumber=parent_phone_no,
                                    alternate_number=alternate_parent_phone_no,
                                    hostel='none',
                                    email=parent_email,
                                    image=f'{settings.MEDIA_ROOT}/profile.png',
                                )
                                user.save()

                                event = Events.objects.create(
                                    username=matric_no,
                                    notification=f"Welcome to Caleb Exeats.",
                                    receiver=parent_email,
                                    tag='success',
                                    date_added_main=f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"

                                )

                                event.save()
                                
                                event = Events.objects.create(
                                    username='admin',
                                    notification=f"You Registered {parent_email}",
                                    receiver='admin',
                                    tag='success',
                                    date_added_main=f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"

                                )

                                event.save()


                                is_reg_parent = True

                            return Response({"message": "student created successfully", "verification": f"registered Student: {is_reg_student}, Registered Parent: {is_reg_parent}", })

                        return Response({"message": "user already exists in student database"})

                    return Response({"message": "user already exists in general database"})

                return Response({"message": "user already exists in user database"})

            return Response({"message": "invalid user category"})
            
                

#==========================GENERAL===============================

class StudentRecentForms(APIView):
    def get(self, request, token, format=None):
        
        is_token = Token.objects.filter(key=token).values()[0]
        username = User.objects.filter(id=is_token['user_id']).values()[0]['username']

        if len(is_token) == 0:
            return Response({'message':'user_not_exist'}) 
        
        user = Allusers.objects.filter(username=username).values()[0]
        email = User.objects.filter(username=username).values()[0]['email']
        hostel = user['hostel']
        usercat = user['usercat']
        phone = user['phonenumber']
        
        if usercat.lower().strip() == 'student' and username[0:2].isnumeric() and username[3:].isnumeric():
            recentforms = Forms.objects.filter(matric_no=username).all()
            serializer = FormsSerializer(recentforms, many=True)
            return Response(serializer.data)
        
        if usercat.lower().strip() == 'porter':
            recentforms = Forms.objects.filter(hostel=hostel).filter(iscancelled=0).all()
            serializer = FormsSerializer(recentforms, many=True)
            return Response(serializer.data)
        
        if usercat.lower().strip() == 'parent':
            
            recentforms = Forms.objects.filter(Q(parentemail=username) | Q(parent_no = phone) | Q(parentemail=email)).filter(iscancelled=0).all()
            serializer = FormsSerializer(recentforms, many=True)
            return Response(serializer.data)
        
        if usercat.lower().strip() == 'saffairs':
            
            recentforms = Forms.objects.filter(iscancelled=0).all()
            serializer = FormsSerializer(recentforms, many=True)
            return Response(serializer.data)
        
        if usercat.lower().strip() == 'security':
            recentforms = Forms.objects.filter(iscancelled=0).all()
            serializer = FormsSerializer(recentforms, many=True)
            return Response(serializer.data)

        else:
            return Response({'message':'invalid_user'})
        
        
class StudentRecentFormsForced(APIView):
    def get(self, request, thing, format=None):
        token,command = thing.split("=|=")
        
    
        is_token = Token.objects.filter(key=token).values()[0]
        username = User.objects.filter(id=is_token['user_id']).values()[0]['username']

        if len(is_token) == 0:
            return Response({'message':'user_not_exist'}) 
        
        user = Allusers.objects.filter(username=username).values()[0]
        email = User.objects.filter(username=username).values()[0]['email']
        hostel = user['hostel']
        usercat = user['usercat']
        phone = user['phonenumber']
        
        if usercat.lower().strip() == 'student' and username[0:2].isnumeric() and username[3:].isnumeric():
            recentforms = Forms.objects.filter(matric_no=username).filter(iscancelled=0).filter(Q(statusPorter=command) | Q(statusParent=command) | Q(statusStudentAffairs=command)).all()
            serializer = FormsSerializer(recentforms, many=True)
            return Response(serializer.data)
        
        if usercat.lower().strip() == 'porter':
            recentforms = Forms.objects.filter(hostel=hostel).filter(iscancelled=0).filter(statusPorter=command).all()
            serializer = FormsSerializer(recentforms, many=True)
            return Response(serializer.data)
        
        if usercat.lower().strip() == 'parent':
            
            recentforms = Forms.objects.filter(Q(parentemail=username) | Q(parent_no = phone) | Q(parentemail=email)).filter(iscancelled=0).filter(statusParent =command).all()
            serializer = FormsSerializer(recentforms, many=True)
            return Response(serializer.data)
        
        if usercat.lower().strip() == 'saffairs':
            
            recentforms = Forms.objects.filter(iscancelled=0).filter(statusStudentAffairs = command).all()
            serializer = FormsSerializer(recentforms, many=True)
            return Response(serializer.data)
        
        if usercat.lower().strip() == 'security':
            recentforms = Forms.objects.filter(iscancelled=0).all()
            serializer = FormsSerializer(recentforms, many=True)
            return Response(serializer.data)

        else:
            return Response({'message':'invalid_user'})
        
        
class SearchRecentForms(APIView):
    def get(self, request, textvariable, format=None):
        searchtext, token = textvariable.split('=|=')
        is_token = Token.objects.filter(key=token).values()[0]
        
        username = User.objects.filter(id=is_token['user_id']).values()[0]['username']
        userData = Allusers.objects.filter(username = username).values()[0]
            
        usercat = userData['usercat']
        hostel = userData['hostel']
        
        if '-' in searchtext and len(searchtext) == 7 and searchtext[0:2].isnumeric():     
            if usercat == 'porter':
                recentforms = Forms.objects.filter(matric_no = searchtext).filter(hostel=hostel).all()
                serializer = FormsSerializer(recentforms, many=True)
                return Response(serializer.data)   
                  
            elif usercat == 'saffairs' or usercat == 'security':
                recentforms = Forms.objects.filter(matric_no = searchtext).all()
                serializer = FormsSerializer(recentforms, many=True)
                return Response(serializer.data)         

        if searchtext[0:6].lower() == "culext" and searchtext[6:].isnumeric():
           if usercat.lower().strip()=='porter':
                recentforms = Forms.objects.filter(id = searchtext.lower().replace('culext','')).filter(hostel=hostel).all()
                serializer = FormsSerializer(recentforms, many=True)
                return Response(serializer.data)
        
           elif usercat == 'saffairs' or usercat == 'security':
                recentforms = Forms.objects.filter(id = searchtext.lower().replace('culext','')).all()
                serializer = FormsSerializer(recentforms, many=True)
                return Response(serializer.data)
            
        else:
            return Response({'message':'invalid_search'})
        
    
    
class AllUserData(APIView):
    def get(self, request, token, format=None):
        try:
            is_token = Token.objects.filter(key=token).values()[0]
            username = User.objects.filter(id=is_token['user_id']).values()[0]['username']

            if len(is_token) == 0:
                return Response({'message':'user_not_exist'}) 
            
            alluser = Allusers.objects.filter(username=username)
            
            usercat = alluser.values()[0]['usercat']
            hostel = alluser.values()[0]['hostel']
            phone_no = alluser.values()[0]['phonenumber']
            email = alluser.values()[0]['email']
            
            if usercat.lower().strip() == "student":
                approved = Forms.objects.filter(matric_no=username).filter(statusPorter='1').filter(statusParent='1').filter(statusStudentAffairs='1').filter(iscancelled=False).values()
                rejected = Forms.objects.filter(matric_no=username).filter(Q(statusPorter='2') | Q(statusParent='2') | Q(statusStudentAffairs='2')).filter(iscancelled=False).values()
                cancelled = Forms.objects.filter(matric_no=username).filter(iscancelled=True)
                
                pendingCount = len(Forms.objects.filter(matric_no=username).filter(Q(statusPorter='0') | Q(statusParent='0') | Q(statusStudentAffairs='0')).values())
                rejectedCount = len(rejected)
                approvedCount = len(approved)
            
                Allusers.objects.filter(username=username).update(pendingexeats=pendingCount, approvedexeats=approvedCount, rejectedexeats=rejectedCount)
                serializer = AllusersSerializer(alluser[0])
                
                return Response(serializer.data)
            
            elif usercat.lower().strip() == "porter":
        
                approved = Forms.objects.filter(hostel=hostel).filter(statusPorter='1').values()
                rejected = Forms.objects.filter(hostel=hostel).filter(statusPorter='2').values()         
                
                pendingCount = len(Forms.objects.filter(hostel=hostel).filter(statusPorter='0').values())
                rejectedCount = len(rejected)
                approvedCount = len(approved)
            
                Allusers.objects.filter(username=username).update(pendingexeats=pendingCount, approvedexeats=approvedCount, rejectedexeats=rejectedCount)

                serializer = AllusersSerializer(alluser[0])
                return Response(serializer.data)
            
            elif usercat.lower().strip() == "parent":
                print(phone_no, email)
                approved = Forms.objects.filter(Q(parent_no=phone_no) | Q(parentemail=email)).filter(statusParent='1').values()
                rejected = Forms.objects.filter(Q(parent_no=phone_no) | Q(parentemail=email)).filter(statusParent='2').values()   
                
                pendingCount = len(Forms.objects.filter(Q(parent_no=phone_no) | Q(parentemail=email)).filter(statusParent='0').values())
                rejectedCount = len(rejected)
                
                approvedCount = len(approved)
                
                Allusers.objects.filter(username=username).update(pendingexeats=pendingCount, approvedexeats=approvedCount, rejectedexeats=rejectedCount)

                serializer = AllusersSerializer(alluser[0])
                
                return Response(serializer.data)
            
            elif usercat.lower().strip() == "saffairs":
    
                pendingCount = len(Forms.objects.filter(iscancelled=False).filter(statusStudentAffairs='0'))
                rejectedCount = len(Forms.objects.filter(iscancelled=False).filter(statusStudentAffairs='2') )
                
                approvedCount = len(Forms.objects.filter(iscancelled=False).filter(statusStudentAffairs='1'))
            
                Allusers.objects.filter(username=username).update(pendingexeats=pendingCount, approvedexeats=approvedCount, rejectedexeats=rejectedCount)

                serializer = AllusersSerializer(alluser[0])
                return Response(serializer.data)
            
            elif usercat.lower().strip() == "security":
                serializer = AllusersSerializer(alluser[0])
                return Response(serializer.data)
            
            elif usercat.lower().strip() == 'superuser':
                serializer = AllusersSerializer(alluser[0])
                return Response(serializer.data)
            
            else:
                return Response({'message':'invalid_user_category'})
            
           
        except Exception:
            return Response({'message':'user_not_exist'}) 
        
        
        
        
class StudentDataCheck(APIView):
    def get(self, request, details, format=None):
        details = details.split('=|=')
        username = details[0]
        matricNo = details[1]
        usercat = Allusers.objects.filter(username=username).values()[0]['usercat']
        if usercat.lower() in higher_ups or usercat.lower() == 'security':
            alluser = Allusers.objects.filter(username=matricNo).values()[0]
            student = Student.objects.filter(matric_no=matricNo).values()[0]
            
            alluser['level'] = student['student_level']
            alluser['college'] = student['college']
            
            alluser['parent_no'] = student['parent_phone_no']
            alluser['alternate_parent_no'] = student['alternate_parent_phone_no']
            alluser['home_address'] = student['home_address']
            
            return Response(alluser)
        
        elif usercat.lower() == 'superuser':
            alluser = Allusers.objects.filter(username=matricNo).values()[0]
            student = Student.objects.filter(matric_no=matricNo).values()[0]
            
            alluser['level'] = student['student_level']
            alluser['college'] = student['college']
            alluser['department'] = student['department']
            
            alluser['parent_no'] = student['parent_phone_no']
            alluser['alternate_parent_no'] = student['alternate_parent_phone_no']
            alluser['home_address'] = student['home_address']
            alluser['parent_email'] = student['parent_email']
            
            return Response(alluser)
        
        return Response({"message":"Unauthorized"})
            
class GetOtherData(APIView):
    def get(self, request,UserID,format=None):
        pass
    
    def post(self, request, *args, **kwargs):
        pass
         
         
class GetUserNotifications(APIView):
    def get(self, request, token, format=None):
        try:
            print('sdfdsf')
            is_token = Token.objects.filter(key=token).values()[0]
            username = User.objects.filter(id=is_token['user_id']).values()[0]['username']
            
            print(username)
            user = Allusers.objects.filter(username=username).values()[0]
            usercat = user['usercat']
            hostel = user['hostel']
            
            print(usercat, hostel)
            if usercat.lower().strip() == 'student':
                notifications = Events.objects.filter(Q(receiver=username) | Q(receiver='all'))
                serializer = EventsSerializer(notifications, many=True)
                return Response(serializer.data)
            
            elif usercat == 'porter':
                notifications = Events.objects.filter(Q(receiver=username) | Q(receiver='all') | Q(receiver=hostel))
                serializer = EventsSerializer(notifications, many=True)
                return Response(serializer.data)
            
            elif usercat == 'saffairs':
                notifications = Events.objects.filter(Q(receiver=username) | Q(receiver='all') | Q(receiver='HU'))
                serializer = EventsSerializer(notifications, many=True)
                return Response(serializer.data)
            
            elif usercat.lower().strip() == 'parent':
                notifications = Events.objects.filter(receiver=username)
                serializer = EventsSerializer(notifications, many=True)
                return Response(serializer.data)
            
            elif usercat.strip() == 'superuser':
                notifications = Events.objects.filter(receiver=username)
                serializer = EventsSerializer(notifications, many=True)
                return Response(serializer.data)
            
            else:
                return Response({"message":"Unauthorized"})
            
        except Exception:
            return Response({"message":"Unauthorized"})
         
            
        
    
class AORRequest(APIView):
    def post(self, request, *args, **kwargs):
        result = request.data
        
        token = result['token']
        username = result['username']
        formpk = result['formpk']
        change = result['change']
        matric_no = result['matric_no']
        
        is_token = Token.objects.filter(key=token).values()[0]
        user = User.objects.filter(id=is_token['user_id']).values()[0]['username']
        
        if user == username:
            usercat = Allusers.objects.filter(username=username).values()[0]['usercat']
            
            if change.lower().strip() == "approve":
                if usercat.lower() == 'porter': 
                    Forms.objects.filter(id=formpk).update(statusPorter = '1')
                    
                    event = Events.objects.create(
                        username = username,
                        notification = f"You Approved a request from {matric_no} (FormID: CULEXT{formpk})",
                        receiver = username,
                        tag = 'success',
                        date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
                
                    )
                    event.save();
                    
                    event = Events.objects.create(
                        username = username,
                        notification = f"Your request has been Approved by your Porter (FormID: CULEXT{formpk})",
                        receiver = matric_no,
                        tag = 'success',
                        date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
                
                    )
                    event.save();
                    return Response({'message':'success'})
                
                
                
                elif usercat.lower() == 'parent':
                    Forms.objects.filter(id=formpk).update(statusParent = '1')
                    
                    event = Events.objects.create(
                        username = username,
                        notification = f"You Approved a request from {matric_no} (FormID: CULEXT{formpk})",
                        receiver = username,
                        tag = 'success',
                        date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
                    )
                    event.save();
                    event = Events.objects.create(
                        username = username,
                        notification = f"Your request has been Approved by your Parent (FormID: CULEXT{formpk})",
                        receiver = matric_no,
                        tag = 'success',
                        date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
                    )
                    event.save();
                    
                    return Response({'message':'success'})
                
                
                
                
                elif usercat.lower() == 'saffairs': 
                    Forms.objects.filter(id=formpk).update(statusStudentAffairs ='1')
                    event = Events.objects.create(
                        username = username,
                        notification = f"You Approved a request from {matric_no} (FormID: CULEXT{formpk})",
                        receiver = username,
                        tag = 'success',
                        date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
                
                    )
                    event.save();
                    
                    event = Events.objects.create(
                        username = username,
                        notification = f"Student Affairs has Approved your Request (FormID: CULEXT{formpk})",
                        receiver = matric_no,
                        tag = 'success',
                        date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
                
                    )
                    event.save();
                    
                    return Response({'message':'success'})
                
                else:
                    return Response({'message':'unauthorized user'})
                
                
            elif change.lower().strip() == 'reject':
                if usercat.lower() == 'porter': 
                    Forms.objects.filter(id=formpk).update(statusPorter = '2')
                    event = Events.objects.create(
                        username = username,
                        notification = f"You Rejected a request from {matric_no} (FormID: CULEXT{formpk})",
                        receiver = username,
                        tag = 'danger',
                        date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
                
                    )
                    event.save();
                    
                    event = Events.objects.create(
                        username = username,
                        notification = f"Your request has been Rejected by your Porter (FormID: CULEXT{formpk})",
                        receiver = matric_no,
                        tag = 'danger',
                        date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
                
                    )
                    event.save();
                    return Response({'message':'success'})
                
                elif usercat.lower() == 'parent':
                    Forms.objects.filter(id=formpk).update(statusParent = '2')
                    event = Events.objects.create(
                        username = username,
                        notification = f"You Rejected a request from {matric_no} (FormID: CULEXT{formpk})",
                        receiver = username,
                        tag = 'danger',
                        date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
                
                    )
                    event.save();
                    
                    event = Events.objects.create(
                        username = username,
                        notification = f"Your request has been Rejected by your Parent (FormID: CULEXT{formpk})",
                        receiver = matric_no,
                        tag = 'danger',
                        date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
                
                    )
                    event.save();
                    return Response({'message':'success'})
                
                elif usercat.lower() == 'saffairs': 
                    
                    Forms.objects.filter(id=formpk).update(statusStudentAffairs ='2')
                    event = Events.objects.create(
                        username = username,
                        notification = f"You Rejected a request from {matric_no} (FormID: CULEXT{formpk})",
                        receiver = username,
                        tag = 'danger',
                        date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
                
                    )
                    event.save();
                    
                    event = Events.objects.create(
                        username = username,
                        notification = f"Student Affairs Rejected your request (FormID: CULEXT{formpk})",
                        receiver = matric_no,
                        tag = 'danger',
                        date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
                
                    )
                    event.save();
                    return Response({'message':'success'})
                
                else:
                    return Response({'message':'unauthorized user'})
                
            else:
                return Response({'message':'invalid'})
            
            
        return Response({'message':'invalid Authentication'})   
        
        
        
        
class FormCreate(APIView):
    def post(self, request, *args, **kwargs):
        
        form = request.data
        
        token = form['token']
        matric_no = form['matric_no']
        exeat_type = form['exeat_type']
        exeat_description = form['description']
        departure_date = form['departure_date']
        arrival_date = form['arrival_date']
        
        is_token = Token.objects.filter(key=token).values()[0]
        user = User.objects.filter(id=is_token['user_id']).values()[0]['username']
        
        if matric_no == user:
            allusers = Allusers.objects.filter(username=matric_no).values()[0]
            form_left_count = int(allusers['forms_left'])
            if form_left_count != 0:
                student_details = Student.objects.filter(matric_no=matric_no).values()[0]
                
                level = student_details['student_level']
                parent_email = student_details['parent_email']
                student_no = allusers['phonenumber']
                hostel = allusers['hostel']
                parent_no = student_details['parent_phone_no']
                department = student_details['department']
                college = student_details['college']
                fullname = f"{allusers['lastname']} {allusers['firstname']} {allusers['middlename']}".strip()
                studentpic =  settings.MAINMEDIANAME+ allusers['image']
                
                
                
                form = Forms.objects.create(
                    matric_no = matric_no,
                    level = level,
                    fullname = fullname,
                    studentpic = studentpic,
                    exeat_description = exeat_description,
                    departure_date = departure_date,
                    arrival_date = arrival_date,
                    exeat_type = exeat_type,
                    hostel = hostel,
                    parent_no = parent_no,
                    parentemail = parent_email,
                    students_no = student_no,
                    department = department,
                    college = college,
                    date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
                )
                
                form.save();
                
                
                
                
                event = Events.objects.create(
                    username = matric_no,
                    notification = f"{fullname} ({matric_no}) Sent a Request",
                    receiver = hostel,
                    tag = 'primary',
                    date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
                )
                event.save();
                
                event = Events.objects.create(
                    username = matric_no,
                    notification = f"You Sent a Request",
                    receiver = matric_no,
                    tag = 'primary',
                    date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
                )
                event.save();
                
                
                
                print(int(form_left_count)-1)
                Allusers.objects.filter(username=matric_no).update(forms_left=int(form_left_count)-1, last_form_sent_day = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year}")
                
                return Response({'message':'success'}) 
            
            return Response({'message':'daily_form_limit_exceeded'})
        
        return Response({'message':'invalid_authentication'})
    
    
    
    
class CancelForm(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        formid = data['form_id']
        token = data['token']
        username = data['username']
        
        
        is_tokened = Token.objects.filter(key=token).values()
        if is_tokened != [] and len(is_tokened) != 0:
            Forms.objects.filter(id=formid).update(iscancelled = 1)
            
            event = Events.objects.create(
                username = username,
                notification = f"You Cancelled a Request (FormID: CULEXT{formid})",
                receiver = username,
                
                tag = 'primary',
                date_added_main = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} on {datetime.now().hour}:{datetime.now().minute}"
                
            )
            event.save();
            
            return Response({'message':'Success'})
        return Response({'message':'An Error Occured'})
        

class FirstLoginCheck(APIView):
    def get(self, request, username, format=None):
        alluser = Allusers.objects.filter(username=username)
        
        if int(alluser.values()[0]['forms_left']) != 2 and f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year}" != alluser.values()[0]['last_form_sent_day']:
            #print('yippeeeeee', alluser.values()[0]['forms_left'])
            Allusers.objects.filter(username=username).update(forms_left=2)
        
        return Response({'message':'reset'})