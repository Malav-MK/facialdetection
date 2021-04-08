"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('register/', views.register, name='register'),
    # path('login/', views.home, name='login'),

    path('view_appointment/',views.ViewAllAppointment,name='ViewAllAppointment'),
    path('view_accept_appointment/',views.ViewApprovedAppointment,name='ViewApprovedAppointment'),
    path('storeuserdetails/',views.storeuser,name='storeuser'),
    path('takeappointment/<int:id>',views.takeappointment,name='takeappointment'),
    path('submitappointment/<int:id>',views.submitappointment,name='submitappointment'),
    path('accept/<int:id>',views.acceptappointment,name='acceptappointment'),
    path('sendanemail/<int:id>',views.sendanemail_accept,name='sendanemail'),
    path('reject/<int:id>',views.rejectappointment,name='rejectappointment'),
    path('sendanemail1/<int:id>',views.sendanemail_reject,name='sendanemail1'),
    path('device/', views.device, name='device'),
    path('system_device/', views.system_device, name='system_device'),
    path('otp_match/<int:id>', views.otp_match, name='otp_match'),
    path('pdf_view/<int:id>', views.pdf_view, name='pdf_view')



]
