from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import PatientRegistrationForm, DoctorRegistrationForm
from .models import User, Patient, Doctor
from patient_app.models import Appointment
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from .models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from finalYearProject.settings import EMAIL_HOST_USER
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from admin_app.models import Specialization, BannedUser
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import datetime
import base64
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


# Create your views here.

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)
    return my_autopct

def landing(request):
    doctor = Doctor.objects.all()
    doctor_count = doctor.count
    patient = Patient.objects.all()
    patient_count = patient.count
    appointment_count = Appointment.objects.all().count

    # labels = '',''

    plist = list(patient.values())
    dlist = list(doctor.values())

    total_users = len(plist) + len(dlist)
    # sample = 60
    # non_users = sample-total_users
    #
    # sizes = [total_users,non_users]
    #
    # users = ['Registered','Not registered']
    #
    # colors = [ '#f5f595' ,  '#66b3ff',  '#99ff99']
    # explode = (0.1,0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    #
    # fig1, ax1 = plt.subplots( subplot_kw=dict(aspect="equal"))  #figsize to set horizontal and vertical distance of pie
    #
    #
    # wedges,text,autotext = ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=make_autopct(sizes), textprops=dict(color="k"),shadow=True, startangle=90)
    #
    # ax1.set_title("Growing users")
    # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #
    # ax1.legend(wedges, users,title="Users",loc="center left",bbox_to_anchor=(0.80, 0.75, 0.5, 0.25))
    #
    # plt.setp(autotext, size=8, weight="bold")
    #
    # plt.savefig('media/users_piechart.png', dpi=100)

    return render(request, 'landing.html', context={'total_users':total_users, 'doctor_count':doctor_count, 'patient_count':patient_count, 'appointment_count':appointment_count})

def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user:
            login(request, user)
            if user.is_admin:
                return redirect('adminHome')
            elif user.is_patient:
                return redirect('patientHome')
            else:
                return HttpResponseRedirect(reverse('doctorHome', args=[user.id]))
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login')

def signUp(request):
    return render(request, "signUp.html")


def patient_registration(request):
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST['username'])
            if user:
                messages.error(request, "User has an account already")
                return redirect('PatientRegistration')
        except User.DoesNotExist:
            request.session["username"]=request.POST['username']
            if request.POST['password1'] == request.POST['password2']:
                try:
                    validate_email(request.POST['email'])
                except ValidationError as e:
                    messages.error(request, ("Bad Email"))
                    return redirect('PatientRegistration')
                request.session["email"] = request.POST['email']
                request.session["password"] = request.POST['password1']
                return HttpResponseRedirect(reverse('PatientSignUp'))
            else:
                messages.error(request, "Password Mismatch!")
                return HttpResponseRedirect(reverse('PatientRegistration'))
    else:
        form = PatientRegistrationForm()
        return render(request, 'patient_registration1.html', {'form': form})


def patient_signup(request):
    if request.method == "POST":
        user = User.objects.create(username=request.session["username"])
        user.email = request.session["email"]
        user.set_password(request.session["password"])
        user.first_name = request.POST['first_name']
        if request.POST['middle_name']:
            user.middle_name = request.POST['middle_name']
        user.last_name = request.POST['last_name']
        user.date_of_birth = request.POST['date_of_birth']
        user.contact_no = request.POST['contact_no']
        user.gender = request.POST['gender']
        user.is_patient = True
        user.save()
        patient = Patient.objects.create(user=user)
        patient.save()
        messages.success(request, ("User Created Successfully!"))
        return redirect('patientHome')
    else:
        form = PatientRegistrationForm()
        return render(request, 'patient_signup.html', {'form': form})


def doctor_registration(request):
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST['username'])
            if user:
                messages.error(request, "User with this username has an account already")
                return redirect('DoctorRegistration')
        except User.DoesNotExist:
            try:
                doctor = Doctor.objects.get(doctor_reg_id=request.POST['doctor_reg_id'])
                if doctor:
                    messages.error(request, "User with this registration id has an account already")
                    return redirect('DoctorRegistration')
            except Doctor.DoesNotExist:
                try:
                    banDoc = BannedUser.objects.get(userid=request.POST["doctor_reg_id"])
                    if banDoc:
                        messages.error(request, "You have been banned. So,you cannot SignUp!")
                        return redirect('DoctorRegistration')
                except BannedUser.DoesNotExist:
                    request.session["username"] = request.POST['username']
                    if request.POST['password1'] == request.POST['password2']:
                        try:
                            validate_email(request.POST['email'])
                        except ValidationError as e:
                            messages.error(request, ("Bad Email"))
                            return redirect('DoctorRegistration')
                        request.session["email"] = request.POST['email']
                        request.session["password"] = request.POST['password2']
                        request.session["reg_id"] = request.POST["doctor_reg_id"]

                        image = request.FILES['header_image']

                        # encoding image to byte64 string to store in session
                        request.session['header_image'] = base64.b64encode(image.read()).decode()

                        # code to retrieve name of the image file
                        image = str(image).split(".")
                        request.session['image_name'] = image[0]

                        return redirect('DoctorSignUp')
                    else:
                        messages.error(request, "Password Mismatch!")
                        return redirect('DoctorRegistration')
    else:
        form = DoctorRegistrationForm()
        return render(request, 'doctor_registration1.html', {'form': form})


def doctor_signup(request):
    if request.method == "POST":
        request.session["first_name"] = request.POST['first_name']
        if request.POST['middle_name']:
            request.session["middle_name"] = request.POST['middle_name']
        else:
            request.session["middle_name"]=""
        request.session["last_name"] = request.POST['last_name']
        request.session["contact_no"] = request.POST['contact_no']
        request.session["gender"] = request.POST['gender']
        request.session["date_of_birth"] = request.POST['date_of_birth']
        request.session["sp"] = request.POST['sp']
        return redirect('DoctorSignUp2')
    else:
        form = DoctorRegistrationForm()
        specialization = Specialization.objects.all()
        return render(request, 'doctor_signup.html', {'form': form, 'specialization': specialization})

def doctor_signup2(request):
    if request.method == "POST":
        user = User.objects.create(username=request.session["username"])
        user.email = request.session["email"]
        user.set_password(request.session["password"])
        user.first_name = request.session['first_name']
        if request.session['middle_name']!="":
            user.middle_name = request.session['middle_name']
        user.last_name = request.session['last_name']
        user.contact_no = request.session['contact_no']
        user.gender = request.session['gender']

        #decoding the string to image again and then using InMemoryUploadedFile to save it into the database
        image = request.session['header_image']
        data = base64.b64decode(image.encode('UTF-8'))
        buf = BytesIO(data)
        img = Image.open(buf)
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        image_name = request.session["image_name"]
        user.header_image = InMemoryUploadedFile(img_io, field_name=None, name=image_name+".jpg", content_type='image/jpeg',
                                            size=img_io.tell, charset=None)


        user.date_of_birth = request.session['date_of_birth']
        user.is_doctor = True
        user.save()
        doctor = Doctor.objects.create(user=user)
        doctor.specialization = request.session['sp']
        doctor.chamber_address = request.POST['chamber_address']
        doctor.doctor_reg_id = request.session["reg_id"]
        doctor.fees = request.POST['fees']
        doctor.experience = request.POST['experience']
        doctor.degrees = request.POST['degrees'].upper()
        doctor.degree_certificate = request.FILES['degree_certificate']
        doctor.save()
        messages.success(request, ("User Created Successfully!"))
        return HttpResponseRedirect(reverse('doctorHome', args=[user.id]))
    else:
        form = DoctorRegistrationForm()
        return render(request, 'doctor_signup2.html', {'form': form})



def password_reset_request(request):
    if request.method == "POST":
        #password_reset_form = PasswordResetForm(request.POST)
        #if password_reset_form.is_valid():
            username = request.POST['username']
            associated_users = User.objects.filter(username=username)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name,c)
                    try:
                        send_mail(subject,email,EMAIL_HOST_USER,[user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid Header Found')
                    return redirect("done/")
    #password_reset_form = PasswordResetForm()
    return render(request=request,template_name="password_reset.html")
