from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('user/change/change-password/', views.ChangePassword.as_view()),
    path('recent-forms/<str:token>/',views.StudentRecentForms.as_view()),
    path('recent-forms/forced/<str:thing>/',views.StudentRecentFormsForced.as_view()),
    path('searched-forms/<str:textvariable>/',views.SearchRecentForms.as_view()),
    path('user-data/<str:token>/',views.AllUserData.as_view()),
    path('account/administrator/user-data/<str:token>/',views.GetUsersData.as_view()),
    path('students-data/<str:details>/',views.StudentDataCheck.as_view()),
    path('notification/<str:token>/',views.GetUserNotifications.as_view()),
    path('form/change/',views.AORRequest.as_view()),
    path('form/create/',views.FormCreate.as_view()),
    path('form/cancel-form/', views.CancelForm.as_view()),
    path('form/descriptions/',views.GetDescriptions.as_view()),
    path('form/departments/',views.GetDepartments.as_view()),
    path('form/colleges/',views.GetColleges.as_view()),
    path('form/hostels/',views.GetHostels.as_view()),
    path('profile/student/<str:username>/',views.ProfileDetails.as_view()),
    path('actions/customTask/',views.CustomTask.as_view()),
    path('actions/bulkTask/',views.BulkTask.as_view()),
    path('upload/',views.ChangeProfileImage.as_view()),
    path('person/logout/',views.Logout.as_view()),
    path('account/register/',views.RegisterUser.as_view()),
    path('account/register/bulk/',views.RegisterStudentBulk.as_view()),
    path('account/register/logs/<str:token>/',views.RegLogs.as_view()),
    path('student/check/<str:username>/',views.FirstLoginCheck.as_view()),
    path('other-data/<str:info>/',views.GetOtherData.as_view()),
    
    
]
