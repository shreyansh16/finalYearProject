from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account_app.models import User,Doctor
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from admin_app.models import Specialization
from patient_app.models import Appointment, Reviews
from finalYearProject.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, BadHeaderError
import datetime
from django.core.paginator import Paginator
from django.utils.datastructures import MultiValueDictKeyError
import os
import requests
from django.http import FileResponse

# Create your views here.
url = "https://www.fast2sms.com/dev/bulkV2"
headers = {
        'cache-control': "no-cache"
    }

def sendSms(message,contact_no):
    ###############

    querystring = {
        "authorization": "x2eVImBiDW9ko54XK1F7AzjfgtPcJTpQryCvNhubR6UsYGEq0OQ6dqMmGhACeas2ONwo8l0DXtL7iyB4",
        "message": message,
        "language": "english",
        "route": "q",
        "numbers": contact_no}

    try:
        response = requests.request("GET", url,
                                    headers=headers,
                                    params=querystring)
        print("SMS Successfully Sent")
    except:
        print("Oops! Something wrong")

    ###################### SMS CHUNK

@login_required
def doctorHome(request, id):
        try:
                doctor = Doctor.objects.get(pk=id)
        except Doctor.DoesNotExist:
                return render(request,"dump.html")

        user = User.objects.get(doctor=doctor)

        present_date = datetime.date.today()
        last_date = present_date - datetime.timedelta(1)

        present_date = present_date.strftime("%Y-%m-%d")
        last_date = last_date.strftime("%Y-%m-%d")

        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%H:%M")

        # today's appointments
        appointment = Appointment.objects.filter(doctor=doctor, a_date=present_date,is_cancelled=False).order_by("a_time")

        # previous days appointments left to mark done
        pending = Appointment.objects.filter(doctor=doctor, a_date=last_date,is_cancelled=False,is_marked=False).order_by("a_time")
        return render(request, "doctorHome.html",
                      context={'appointment': appointment, 'doctor': doctor, 'user': user, 'pending' : pending, 'current_time':current_time})

@login_required
def updateDocProfile(request, id):
        user = User.objects.get(pk=id)
        doctor = Doctor.objects.get(user=user)
        image = user.header_image
        degree_certificate = doctor.degree_certificate
        if request.method == "POST":
                user.first_name = request.POST["first_name"]
                user.middle_name = request.POST["middle_name"]
                user.last_name = request.POST["last_name"]
                user.contact_no = request.POST["contact_no"]
                user.email = request.POST["email"]
                user.gender = request.POST["gender"]
                try:
                        if request.FILES["header_image"]:
                                if image:
                                        if os.path.exists(image.path):  # to remove the image source and replace it with the new image
                                                os.remove(image.path)
                                user.header_image = request.FILES["header_image"]
                except MultiValueDictKeyError:
                        if image:
                                user.header_image = image
                user.save()
                doctor.specialization = request.POST["sp"]
                doctor.fees = request.POST["fees"]
                doctor.chamber_address = request.POST["chamber_address"]
                doctor.experience = request.POST["experience"]
                doctor.degrees = request.POST["degrees"].upper()
                doctor.bio = request.POST["bio"]
                try:
                        if request.FILES["degree_certificate"]:
                                if degree_certificate:
                                        if os.path.exists(degree_certificate.path):  # to remove the image source and replace it with the new image
                                                os.remove(degree_certificate.path)
                                doctor.degree_certificate = request.FILES["degree_certificate"]
                except MultiValueDictKeyError:
                        if degree_certificate:
                                doctor.degree_certificate = degree_certificate
                doctor.save()
                messages.error(request, "Your Profile Details have been successfully updated!")
                return HttpResponseRedirect(reverse('viewDocProfile', args=[id]))
        else:
                specialization = Specialization.objects.all()
                return render(request, 'updateDocProfile.html', context={'user': user, 'specialization':specialization})

@login_required
def viewDocProfile(request, id):
        try:
                doctor = Doctor.objects.get(pk=id)
        except Doctor.DoesNotExist:
                return render(request, "dump.html")

        #total likes
        total_likes = doctor.total_likes()

        #total dislikes
        total_dislikes = doctor.total_dislikes()

        age = doctor.user.calculateAge()

        return render(request, 'viewDocProfile.html', context={'doctor': doctor,'age':age, 'likes':total_likes, 'dislikes':total_dislikes})

@login_required
def cancelAppointment(request, id):
        try:
                appointment = Appointment.objects.get(pk=id)
        except Appointment.DoesNotExist:
                return render(request, "dump.html")
        return render(request, 'askCancellation.html', context={'appid':id,'appointment':appointment})

@login_required
def cancelAppointment1(request, id):
        try:
                appointment = Appointment.objects.get(pk=id)
        except Appointment.DoesNotExist:
                return render(request, "dump.html")

        current_time = datetime.datetime.now()
        present_date = datetime.date.today()
        present_date = present_date.strftime("%Y-%m-%d")
        current_time = current_time.strftime("%H:%M")

        if appointment.doctor.user == request.user:

                if appointment.a_time <= current_time and appointment.a_date <= present_date:
                        subject = 'Appointment Cancellation for Dr.' + ' ' + appointment.doctor.user.first_name + ' ' + appointment.doctor.user.last_name
                        message = 'Your appointment has been cancelled for Dr.' + ' ' + appointment.doctor.user.first_name + ' ' + appointment.doctor.user.last_name + ' because ' + appointment.p_first_name + ' '
                        if appointment.p_middle_name:
                                message += appointment.p_middle_name

                        message += ' ' + appointment.p_last_name + ' did not turn up at the given date and time.' + '\n' + \
                                   'Appointment Date: ' + appointment.a_date + '\n' + \
                                   'Appointment Time: ' + appointment.a_time

                else:
                        subject = 'Appointment Cancellation for Dr.' + ' ' + appointment.doctor.user.first_name + ' ' + appointment.doctor.user.last_name
                        message = 'Your appointment has been cancelled for Dr.' + ' ' + appointment.doctor.user.first_name + ' ' + appointment.doctor.user.last_name + '.\n\n' + \
                                  'Patient Name: ' + appointment.p_first_name + ' '
                        if appointment.p_middle_name:
                                message += appointment.p_middle_name

                        message += ' ' + appointment.p_last_name + '\n' + \
                                   'Appointment Date: ' + appointment.a_date + '\n' + \
                                   'Appointment Time: ' + appointment.a_time +'\n\n'+'For booking any further appointments please visit our website'

                        doc_subject = 'Appointment Cancellation for Patient ' + appointment.p_first_name + ' ' + appointment.p_last_name
                        doc_message = 'Your Appointment has been Cancelled for Patient ' + appointment.p_first_name + ' '

                        if appointment.p_middle_name:
                                doc_message += appointment.p_middle_name

                        doc_message += ' ' + appointment.p_last_name + '\n' + \
                                       'Appointment Date: ' + appointment.a_date + '\n' + \
                                       'Appointment Time: ' + appointment.a_time

                        #mail to doctor only
                        try:
                                send_mail(doc_subject,
                                          doc_message, EMAIL_HOST_USER, [appointment.doctor.user.email],
                                          fail_silently=False)
                        except BadHeaderError:
                                return HttpResponse("Unable to Send an Email to The Doctor")





                # overall mail to patients
                try:
                        send_mail(subject,
                                  message, EMAIL_HOST_USER, [appointment.p_email], fail_silently=False)
                except BadHeaderError:
                        return HttpResponse("Unable to Send an Email to The Patient")

                #send sms to patient
                sendSms(message,appointment.p_contact_no)

                appointment.is_cancelled = True
                appointment.save()

        present_date = datetime.date.today()
        present_date = present_date.strftime("%Y-%m-%d")

        if appointment.a_date > present_date:
                return HttpResponseRedirect(reverse('docUpcomingApp', args=[appointment.doctor.user.id]))
        else:
                return HttpResponseRedirect(reverse('doctorHome', args=[appointment.doctor.user.id]))

@login_required
def docUpcomingApp(request, id):
        try:
                doctor = Doctor.objects.get(pk=id)
        except Doctor.DoesNotExist:
                return render(request,"dump.html")

        user = User.objects.get(doctor=doctor)
        present_date = datetime.date.today()
        present_date = present_date.strftime("%Y-%m-%d")
        appointment = Appointment.objects.filter(doctor=doctor, a_date__gt=present_date,is_cancelled=False).order_by("a_date","a_time")
        count = appointment.count()
        paginator = Paginator(appointment, 10)  # to add paging to the website
        page = request.GET.get('pg')
        all_appointment = paginator.get_page(page)
        return render(request, "docUpcomingApp.html",
                      context={'appointment': all_appointment, 'doctor': doctor, 'user': user, 'count':count})


@login_required
def docHistoryApp(request, id):
        try:
                doctor = Doctor.objects.get(pk=id)
        except Doctor.DoesNotExist:
                return render(request, "dump.html")

        present_date = datetime.date.today()

        last_date = present_date - datetime.timedelta(30)
        last_date = last_date.strftime("%Y-%m-%d")

        previous_date = present_date - datetime.timedelta(1)
        previous_date = previous_date.strftime("%Y-%m-%d")

        # history constitutes of appointments upto day before yesterday that are not cancelled and those appointments of yesterday that have been marked done
        comb_appointment = Appointment.objects.filter(doctor=doctor, a_date__gte=last_date, a_date__lt=present_date,is_cancelled=False,is_marked=True) | Appointment.objects.filter(doctor=doctor, a_date__gte=last_date, a_date__lt=previous_date,is_cancelled=False)
        appointment = comb_appointment.order_by("-a_date")

        count = appointment.count()
        paginator = Paginator(appointment, 10)  # to add paging to the website
        page = request.GET.get('pg')
        all_appointment = paginator.get_page(page)
        return render(request, 'docHistoryApp.html', context={'appointment': all_appointment, 'doctor': doctor, 'count':count})

@login_required
def docCancelledApp(request, id):
        try:
                doctor = Doctor.objects.get(pk=id)
        except Doctor.DoesNotExist:
                return render(request,"dump.html")

        present_date = datetime.date.today()
        last_date = present_date - datetime.timedelta(30)
        last_date = last_date.strftime("%Y-%m-%d")

        appointment = Appointment.objects.filter(doctor=doctor, a_date__gte=last_date, is_cancelled=True,is_marked=False).order_by("-a_date")
        count = appointment.count()
        paginator = Paginator(appointment, 10)  # to add paging to the website
        page = request.GET.get('pg')
        all_appointment = paginator.get_page(page)
        return render(request, 'docCancelledApp.html', context={'appointment': all_appointment, 'doctor': doctor, 'count':count})

@login_required
def docReviews(request, id):
        try:
                user = User.objects.get(pk=id)
                doctor = Doctor.objects.get(user=user)
        except Doctor.DoesNotExist:
                return render(request, "dump.html")
        rev = Reviews.objects.filter(doctor=doctor)
        count = rev.count()

        # total likes
        total_likes = doctor.total_likes()

        # total dislikes
        total_dislikes = doctor.total_dislikes()

        return render(request, "docReviews.html", context={'rev':rev,'doctor':doctor,'count':count,'likes':total_likes,'dislikes':total_dislikes})

@login_required
def doneAppointment(request, id):
        try:
                appointment = Appointment.objects.get(pk=id)
        except Appointment.DoesNotExist:
                return render(request, "dump.html")

        if appointment.doctor.user == request.user:
                appointment.is_marked=True
                appointment.save()
        return HttpResponseRedirect(reverse('doctorHome', args=[appointment.doctor.user.id]))

def viewPdf(request, id):
        doctor = Doctor.objects.get(pk=id)
        if doctor.degree_certificate:
                filepath = os.path.join('media', str(doctor.degree_certificate))
                return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
        else:
                return HttpResponse("Error: No File Found!")
