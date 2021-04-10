from django.conf import settings
from django.core.mail import send_mail

from django.shortcuts import render,redirect
from face_recognition_code import recognition
from django.shortcuts import render
from .models import User,Appointment
# Create your views here.
from django.http import HttpResponse
from django.contrib import messages
import cv2
import random
from django.shortcuts import render
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa


def home(request):
    if request.method == 'POST' and 'uid' in request.POST and 'pass' in request.POST:
        u_name = request.POST.get('uid')
        u_pass = request.POST.get('pass')
        try:
            user=User.objects.get(name=u_name)
        except User.DoesNotExist:
            user = None
        if user is not None:
            if u_name == "admin":
                if u_pass == "admin":
                    return render(request,'View_option.html')
                else:
                    messages.info(request, 'Password Does not match.')
            else:
                if u_pass==user.password1:
                    # import pdb;pdb.set_trace()
                    return render(request,'appointment.html',{"id":user.id})
                else:
                    messages.info(request, 'Password Does not match.')
        else:
            messages.info(request,'User Does not exist.')

    return render(request,'index.html')

def register(request):
    return render(request, "register.html")


def storeuser(request):
    if request.method == "POST":
        name = request.POST.get('uid')
        password1 = request.POST.get('pswd1')
        password2 = request.POST.get('pswd2')
        contact = request.POST.get('ucontact')
        email_id= request.POST.get('uemail')

        if password1 == password2:
            if User.objects.filter(name=name).exists():
                messages.info(request, 'username taken')
                return redirect('register')
            elif User.objects.filter(email_id=email_id).exists():
                messages.info(request, 'email taken')
                return redirect('register')
            else:
                form_info = User(name=name, password1=password1, password2=password2, contact=contact,
                                          email_id=email_id)
                form_info.save()
                print('user created')
                # return redirect('')
        else:
            messages.info(request, 'password not matching')
            return redirect('register')
    else:
        return render(request, "index.html")

    return render(request,'index.html')

# def storeuser(request):
#
#     u_data_name=[]
#     user_obj=User.objects.all().values_list('name',flat=True)
#
#     u_name = request.POST.get('uid')
#     u_pass1 = request.POST.get('upassword1')
#     u_pass2 = request.POST.get('upassword2')
#     u_contact = request.POST.get('ucontact')
#     u_email = request.POST.get('uemail')
#     for i in user_obj:
#         u_data_name.append(i)
#
#     if u_pass1==u_pass2:
#         if u_name in u_data_name:
#             messages.info(request, 'User name already not exist.')
#             return render(request, 'register.html')
#         else:
#             user=User(name=u_name,password=u_pass,contact=u_contact,email_id=u_email)
#             user.save()
#             return render(request, 'index.html')
#     else:
#         messages.info(request, 'Password is not match')
#         return render(request, 'register.html')

def takeappointment(request,id):
    return render(request,'appointment_form.html',{"id":id})

def submitappointment(request,id):
    visit_type = request.POST.get('visit')
    description = request.POST.get('desc')
    date_from = request.POST.get('date_from')
    date_to = request.POST.get('date_to')
    cam = cv2.VideoCapture(0)

    face_detector = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
    count = 0
    while (True):
        ret, img = cam.read()
        faces = face_detector.detectMultiScale(img, 1.3, 5)
        for (x, y, w, h) in faces:
            x1 = x
            y1 = y
            x2 = x + w
            y2 = y + h
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
            count += 1
            user = User.objects.get(id=id)
            cv2.imwrite("./static/images/" + user.name + ".jpg", img[y1:y2, x1:x2])
            cv2.imshow('image', img)
        k = cv2.waitKey(200) & 0xff
        if k == 27:
            break
        elif count >= 1:
            break
    cam.release()
    cv2.destroyAllWindows()
    user=User.objects.get(id=id)
    appoinments_obj=Appointment(visit_type=visit_type,description=description,date_from=date_from,date_to=date_to,user_id=user)
    appoinments_obj.save()
    messages.info(request, 'Appointment submitted sucessfully.')
    return render(request,'appointment.html',{"id":id})

def ViewAllAppointment(request):
    appointments_obj = Appointment.objects.filter(is_Active=False)
    return render(request,'View_appointment.html',{"data":appointments_obj})

def ViewApprovedAppointment(request):
    appointments_obj = Appointment.objects.filter(is_Active=True,otp_Number__isnull=False)
    return render(request, 'View_approved_appointment.html', {"data": appointments_obj})

def acceptappointment(request,id):

    appointment_obj=Appointment.objects.get(id=id)
    user_obj = User.objects.get(id=appointment_obj.user_id.id)
    start_Date= appointment_obj.date_from
    end_Date=appointment_obj.date_to
    start_Date=start_Date.strftime("%Y-%m-%d")
    end_Date=end_Date.strftime("%Y-%m-%d")

    return render(request,'Accept_request_form.html',{"user":user_obj,"appointment":appointment_obj,"startdate":start_Date,"enddate":end_Date,"id":id})

def rejectappointment(request,id):

    appointment_obj=Appointment.objects.get(id=id)
    user_obj = User.objects.get(id=appointment_obj.user_id.id)
    return render(request,'reject_request_form.html',{"user":user_obj,"id":id})


def sendanemail_accept(request,id):
    otp = random.randint(1000, 9999)
    appointment_obj=Appointment.objects.get(id=id)
    appointment_obj.otp_Number = otp
    appointment_obj.is_Active = True
    to_email = request.POST.get('toemail')
    meeting_date = request.POST.get('date')
    email_from = settings.EMAIL_HOST_USER
    appointment_obj.confirm_date=meeting_date
    appointment_obj.save()
    message='Thank you for your interest.I welcome to the opportunity to meet with you on '+ meeting_date +' and you otp is '+str(otp)+'.The specified date and time are convenient to us, so we shall meet at office as scheduled.I genuinely appreciate a prompt confirmation from your side.'
    send_mail('Meeting date at The Big Office company', message, email_from, [to_email], fail_silently=False)
    return render(request,'View_option.html')

def sendanemail_reject(request,id):
    to_email = request.POST.get('toemail')
    email_from = settings.EMAIL_HOST_USER
    email_body = request.POST.get('Email_body')
    Appointment.objects.filter(id=id).delete()
    send_mail('Meeting date at The Big Office company', email_body, email_from,[to_email] ,
              fail_silently=False)
    return render(request,'View_option.html')

def device(request):
    return render(request,'Device_face_detection.html')

def system_device(request):
    input_embedding = recognition.create_input_image_embeddings()

    name, faces = recognition.recognize_faces_in_cam(input_embedding)
    if name!=None:
        print(name)
        print(faces)
        user_obj= User.objects.get(name=name)
        appointment_obj=Appointment.objects.filter(user_id=user_obj)
        return render(request, 'Otp_form.html', {"user_obj": user_obj})
    else:
        return redirect('system_device')

def otp_match(request,id):
    app_obj=Appointment.objects.filter(user_id=id)
    otp_list=[]
    for i in app_obj:
        if i.otp_Number!=None:
            otp_list.append(i.otp_Number)
    if int(request.POST.get('otp')) in otp_list:
        appoinment_obj=Appointment.objects.get(otp_Number=request.POST.get('otp'))
        return redirect('pdf_view',id=appoinment_obj.pk)
    else:
        return HttpResponse("Otp is not match")


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


def pdf_view(request,id):
    appointment_obj=Appointment.objects.filter(pk=id).values('confirm_date','visit_type')[0]
    app_obj=Appointment.objects.get(pk=id)
    appointment_obj['name']=app_obj.user_id.name
    pdf = render_to_pdf('D:/final/Project_G19/templates/pdf_template.html', appointment_obj)
    return HttpResponse(pdf, content_type='application/pdf')