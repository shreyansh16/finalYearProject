from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from account_app.models import User, Patient, Doctor
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from admin_app.models import Specialization
from .forms import AppointmentForm, ReviewForm, DocumentUplaodForm
import datetime
from patient_app.models import Appointment, Reviews, DocumentUpload
from finalYearProject.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.utils.datastructures import MultiValueDictKeyError
import os
from django.db.models import Q
import requests

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

head_spl = Specialization.objects.all()
head_doc = Doctor.objects.all()


@login_required
def patientHome(request): #dynamic list that changes on the increasing demand of the specialization
    specialization = Specialization.objects.raw("select * from admin_app_specialization order by count desc limit 6")
    return render(request, "patientHome.html",context={'specialization':specialization,'head_spl':head_spl,'head_doc':head_doc})

@login_required
def specializationList(request):
    specialization = Specialization.objects.all().order_by("category")
    paginator = Paginator(specialization, 8)  # to add paging to the website
    count = specialization.count()
    page = request.GET.get('pg')
    all_specialization = paginator.get_page(page)
    return render(request, "specializationList.html", context={'specialization':all_specialization,'count':count, 'head_spl':head_spl,'head_doc':head_doc})

@login_required
def updatePatProfile(request, id):
    user = User.objects.get(pk=id)
    image = user.header_image
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
        patient = Patient.objects.get(user=user)
        patient.save()
        messages.error(request, "Your Profile Details have been successfully updated!")

        return HttpResponseRedirect(reverse('viewPatProfile', args=[id]))
    else:
        return render(request, 'updatePatProfile.html', context={'user': user, 'head_spl':head_spl,'head_doc':head_doc})

@login_required
def viewPatProfile(request, id):
    try:
        patient = Patient.objects.get(pk=id)
    except Patient.DoesNotExist:
        return render(request, "dump.html") #dump end
    age = patient.user.calculateAge()
    return render(request, 'viewPatProfile.html', context={'patient': patient,'age':age, 'head_spl':head_spl,'head_doc':head_doc})

@login_required
def categoryList(request,cat):
    doctor = Doctor.objects.filter(specialization=cat).order_by("user__first_name")
    count = doctor.count()
    paginator = Paginator(doctor, 5)  # to add paging to the website
    page = request.GET.get('pg')
    all_doctor = paginator.get_page(page)
    return render(request,"categoryList.html",{'doctor':all_doctor, 'count':count, 'head_spl':head_spl,'head_doc':head_doc,'cat':cat})

@login_required
def checkDocProfile(request, id):
    doctor = Doctor.objects.get(pk=id)
    total_likes = doctor.total_likes() # function to get total likes from the model directly
    patient = Patient.objects.get(pk=request.user.id)

    # filtering the records on basis of the previous appointments
    present_date = datetime.date.today()

    previous_date = present_date - datetime.timedelta(1)  # to get the previous day date
    previous_date = previous_date.strftime("%Y-%m-%d")

    appointment = Appointment.objects.filter(doctor=doctor,patient=patient,a_date__lt = present_date, is_cancelled=False, is_marked=True) | Appointment.objects.filter(doctor=doctor,patient=patient,a_date__lt = previous_date, is_cancelled=False)

    # to check if the patient has liked the doctor or not
    has_likes = Doctor.objects.filter(likes=patient)
    has_dislikes = Doctor.objects.filter(dislikes=patient)

    #reviews list
    reviews = Reviews.objects.filter(doctor=doctor)
    count = reviews.count()

    return render(request, 'checkDocProfile.html', context={'doctor': doctor, 'total_likes':total_likes, 'appointment':appointment, 'has_likes':has_likes, 'has_dislikes':has_dislikes, 'reviews':reviews, 'count':count, 'head_spl':head_spl,'head_doc':head_doc})

@login_required
def bookAppointment(request, id, patid):
    try:
        doctor = Doctor.objects.get(pk=id)
    except Doctor.DoesNotExist:
        return render(request, "dump.html")
    try:
        patient = Patient.objects.get(pk=patid)
    except Patient.DoesNotExist:
        return render(request, "dump.html")
    if request.method == "POST":
        p_date = request.POST["ad"] #taking date in dd-mm-yyyy format and converting it into yyyy-mm-dd
        p_date = datetime.datetime.strptime(p_date, '%d-%m-%Y')
        p_date = p_date.strftime("%Y-%m-%d")
        p_time = request.POST["a_time"]
        try:
            #if appointment exists with the chosen date and time then a different slot has to be chosen
            appointment = Appointment.objects.get(doctor=doctor, a_date=p_date, a_time=p_time)
            if appointment:
                messages.error(request, "Please choose a different slot for Doctor's Appointment!")
                return HttpResponseRedirect(reverse('bookAppointment', args=[id,patid]))
        except Appointment.DoesNotExist:
            #appointment = Appointment.objects.create(doctor=doctor, a_date=p_date, a_time=p_time, patient=patient)
            request.session["p_date"] = p_date
            request.session["p_time"] = p_time
            request.session["docid"] = id
            request.session["patid"] = patid
            #appointment.save()
            return redirect('patientInfo')
    else:
        form = AppointmentForm()
        present_date = datetime.date.today()
        date_choices = []
        for i in range(1, 8): # function to take only the next seven days of the week
            days = datetime.timedelta(i)
            new_date = present_date + days
            date_choices.append(new_date.strftime("%d-%m-%Y"))
        return render(request, "bookAppointment.html", {'form': form, 'a_date': date_choices, 'doctor': doctor, 'patient':patient, 'head_spl':head_spl,'head_doc':head_doc})

#decide = False

@login_required
def patientInfo(request):
    try:
        doctor = Doctor.objects.get(pk=request.session["docid"])
    except Doctor.DoesNotExist:
        return render(request, "dump.html")
    try:
        patient = Patient.objects.get(pk=request.session["patid"])
    except Patient.DoesNotExist:
        return render(request, "dump.html")
    if request.method == "POST":
        p_date = request.session["p_date"]
        p_time = request.session["p_time"]
        appointment = Appointment.objects.create(doctor=doctor,a_date=p_date,a_time=p_time,patient=patient)
        appointment.p_age = request.POST["p_age"]
        appointment.p_email = request.POST["p_email"]
        appointment.p_first_name = request.POST["p_first_name"]
        appointment.p_last_name = request.POST["p_last_name"]
        appointment.p_gender = request.POST["gender"]
        appointment.p_contact_no = request.POST["p_contact_no"]
        if request.POST["p_middle_name"] != "":
            appointment.p_middle_name = request.POST["p_middle_name"]
        if request.POST["visit_reason"] != "":
            appointment.visit_reason = request.POST["visit_reason"]
        spl = Specialization.objects.get(category = appointment.doctor.specialization)
        spl.count = spl.count + 1 # increase in count = increase in demand of that specialization
        spl.save()
        appointment.save()

        subject = 'Appointment Booking Confirmation for Dr.'+' '+doctor.user.first_name+' '+doctor.user.last_name
        message = 'Your Booking has been Confirmed for Dr.'+' '+doctor.user.first_name+' '+doctor.user.last_name+'.\n\n'+\
                  'Patient Name: '+appointment.p_first_name+' '
        if appointment.p_middle_name:
            message+=appointment.p_middle_name

        message+=' '+appointment.p_last_name+'\n'+\
                  'Appointment Date: '+appointment.a_date+'\n'+\
                  'Appointment Time: '+appointment.a_time+'\n'+'Doctor Chamber Information: \n' +doctor.chamber_address +'\n\n' \
                        +'For any further changes to your appointment contact our customer support at the details given below:-'+'\n\n'+\
                  'Email Id: '+ EMAIL_HOST_USER

        doc_subject = 'Appointment Booked for Patient '+ appointment.p_first_name+' '+appointment.p_last_name
        doc_message = 'You have an appointment with Patient '+ appointment.p_first_name
        doc_message += ' ' + appointment.p_last_name + '\n' + \
                   'Appointment Date: ' + appointment.a_date + '\n' + \
                   'Appointment Time: ' + appointment.a_time +'\n\n' + 'To check on your upcoming appointments. Please click the given link:'+'\n'+\
                       'http://127.0.0.1:8000/doctorHome/docUpcomingApp/'+str(doctor.user.id)+'/'

        #mail to doctor
        try:
            send_mail(doc_subject,
                      doc_message, EMAIL_HOST_USER, [appointment.doctor.user.email], fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Unable to Send an Email to Doctor!')

        #mail to patient
        try:
            send_mail(subject,
                      message, EMAIL_HOST_USER, [appointment.p_email], fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Unable to Send an Email to Patient!')

        #send sms to patient
        sendSms(message,appointment.p_contact_no)

        return render(request, 'appointmentConfirm.html', context={'appointment':appointment, 'doctor':doctor, 'head_spl':head_spl,'head_doc':head_doc})
    else:
       #form = AppointmentForm(instance=appointment)
       #if not decide:
       #    return render(request, "patientInfo.html", {'doctor': doctor})
       #else:
           return render(request, "patientInfo.html", {'doctor': doctor, 'patient': patient, 'head_spl':head_spl,'head_doc':head_doc})

@login_required
def currentApp(request, id):
    try:
        patient = Patient.objects.get(pk=id)
    except Patient.DoesNotExist:
        return render(request,"dump.html")

    present_date = datetime.date.today()
    present_date = present_date.strftime("%Y-%m-%d")

    current_time = datetime.datetime.now()
    current_time = current_time.strftime("%H:%M")

    comb_appointment = Appointment.objects.filter(patient=patient,a_date__gt = present_date ,is_cancelled=False)
    appointment = comb_appointment.order_by("a_date","a_time")

    today_appointment = Appointment.objects.filter(patient=patient,a_date = present_date ,is_cancelled=False).order_by("a_time")

    return render(request, 'currentApp.html',context={'appointment':appointment,'patient':patient,'today_appointment': today_appointment, 'current_time' : current_time, 'head_spl':head_spl,'head_doc':head_doc})


@login_required
def historyApp(request, id):
    try:
        patient = Patient.objects.get(pk=id)
    except Patient.DoesNotExist:
        return render(request,"dump.html")

    present_date = datetime.date.today()
    last_date = present_date - datetime.timedelta(90) # to show last 3 months appointment history 3*30
    last_date = last_date.strftime("%Y-%m-%d")

    previous_date = present_date - datetime.timedelta(1) # to get the previous day date
    previous_date = previous_date.strftime("%Y-%m-%d")

    #current_time = datetime.datetime.now()
    #current_time = current_time.strftime("%H:%M")

    comb_appointment = Appointment.objects.filter(patient=patient,a_date__gte = last_date,a_date__lt = present_date, is_cancelled=False, is_marked=True) | Appointment.objects.filter(patient=patient,a_date__gte = last_date,a_date__lt = previous_date, is_cancelled=False)
    appointment = comb_appointment.order_by("-a_date")


    count = appointment.count()
    paginator = Paginator(appointment, 5)  # to add paging to the website
    page = request.GET.get('pg')
    all_appointment = paginator.get_page(page)
    return render(request, 'historyApp.html', context={'appointment': all_appointment, 'patient': patient, 'count':count, 'head_spl':head_spl,'head_doc':head_doc})

@login_required
def cancelledApp(request,id):
    try:
        patient = Patient.objects.get(pk=id)
    except Patient.DoesNotExist:
        return render(request,"dump.html")

    present_date = datetime.date.today()
    last_date = present_date - datetime.timedelta(90)
    last_date = last_date.strftime("%Y-%m-%d")

    appointment = Appointment.objects.filter(patient=patient,a_date__gte = last_date,is_cancelled=True).order_by("-a_date")
    count = appointment.count()
    paginator = Paginator(appointment, 5)  # to add paging to the website
    page = request.GET.get('pg')
    all_appointment = paginator.get_page(page)
    return render(request, 'cancelledApp.html',context={'appointment': all_appointment, 'patient': patient, 'count': count, 'head_spl':head_spl,'head_doc':head_doc})

@login_required
def patCancelAppointment(request, id):
    try:
        appointment = Appointment.objects.get(pk=id)
    except Appointment.DoesNotExist:
        return render(request, "dump.html")
    return render(request, 'patAskCancellation.html', context={'appid': id,'appointment':appointment, 'head_spl':head_spl,'head_doc':head_doc})

@login_required
def patCancelAppointment1(request, id):
    try:
        appointment = Appointment.objects.get(pk=id)
    except Appointment.DoesNotExist:
        return render(request, "dump.html")

    if appointment.patient.user == request.user:  # to check if the user is the correct user associated with that app

        doc_subject = 'Appointment Cancellation for Patient:' + ' ' + appointment.p_first_name + ' ' + appointment.p_last_name
        doc_message = 'Your appointment has been cancelled for Patient' + ' ' + appointment.p_first_name + ' ' + appointment.p_last_name + '.' + '\n\n'

        doc_message += 'Appointment Date: ' + appointment.a_date + '\n' + \
                   'Appointment Time: ' + appointment.a_time

        subject = 'Appointment Cancellation for Dr.' + ' ' + appointment.doctor.user.first_name + ' ' + appointment.doctor.user.last_name
        message = 'Your appointment has been cancelled for Dr.' + ' ' + appointment.doctor.user.first_name + ' ' + appointment.doctor.user.last_name + '.\n\n' + \
                  'Patient Name: ' + appointment.p_first_name + ' '
        if appointment.p_middle_name:
            message += appointment.p_middle_name

        message += ' ' + appointment.p_last_name + '\n' + \
                   'Appointment Date: ' + appointment.a_date + '\n' + \
                   'Appointment Time: ' + appointment.a_time + '\n\n' + 'For booking any further appointments please visit our website.'

        #mail to patient
        try:
            send_mail(subject,
                      message, EMAIL_HOST_USER, [appointment.p_email], fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Unable to Send an Email to Patient!')

        #send sms to patient part 1
        sendSms(message,appointment.p_contact_no)

        #mail to doctor
        try:
            send_mail(doc_subject,
                      doc_message, EMAIL_HOST_USER, [appointment.doctor.user.email], fail_silently=False)
        except BadHeaderError:
            return HttpResponse("Unable to Send an Email to The Doctor!")
        appointment.is_cancelled = True
        appointment.save()

    return HttpResponseRedirect(reverse('currentApp', args=[appointment.patient.user.id]))

@login_required
def likeDoc(request, id, patid):
    user = User.objects.get(pk=id)
    doctor = Doctor.objects.get(user=user)

    patient = Patient.objects.get(pk=request.user.id)
    has_like = Doctor.objects.filter(likes=patient)

    if has_like:                                    #if the user already has liked the doctor pressing the same
        doctor.likes.remove(request.user.patient)   #button ensures that like to change to un-like
    else:                                           # if the user has liked then like count increases and dislike
        doctor.likes.add(request.user.patient)      # count automatically decreases
        doctor.dislikes.remove(request.user.patient)
    return HttpResponseRedirect(reverse("checkDocProfile", args=[id]))

@login_required
def dislikeDoc(request, id, patid):
    user = User.objects.get(pk=id)
    doctor = Doctor.objects.get(user=user)

    patient = Patient.objects.get(pk=request.user.id)
    has_dislike = Doctor.objects.filter(dislikes=patient)

    if has_dislike:                                     #if the user already has disliked the doctor pressing the same
        doctor.dislikes.remove(request.user.patient)    #button ensures that like to change to un-dislike
    else:                                               # if the user has disliked then dislike count increases and like
        doctor.dislikes.add(request.user.patient)       # count automatically decreases
        doctor.likes.remove(request.user.patient)
    return HttpResponseRedirect(reverse("checkDocProfile", args=[id]))

@login_required
def giveReview(request, id): # reveiws can only be given if the patient has an appointment with the doctor and is_cancelled=False
    patient = Patient.objects.get(pk=request.user.id)
    try:
        user = User.objects.get(pk=id)
        doctor = Doctor.objects.get(user=user)
    except Doctor.DoesNotExist:
        return render(request, "dump.html")
    if request.method == "POST":
        r = Reviews.objects.create(doctor=doctor,patient=patient)
        r.review = request.POST["review"]
        r.save()
        return HttpResponseRedirect(reverse('checkDocProfile', args=[id]))
    else:
        form = ReviewForm()
        present_date = datetime.date.today()
        previous_date = present_date - datetime.timedelta(1)  # to get the previous day date
        previous_date = previous_date.strftime("%Y-%m-%d")
        appointment = Appointment.objects.filter(doctor=doctor,patient=patient,a_date__lt = present_date, is_cancelled=False, is_marked=True) | Appointment.objects.filter(doctor=doctor,patient=patient,a_date__lt = previous_date, is_cancelled=False)
        return render(request, 'reviews.html', context={'form':form, 'appointment':appointment ,'doctor':doctor, 'head_spl':head_spl,'head_doc':head_doc})

@login_required
def getResult(request):
    if request.method == "POST":
        name = request.POST["tags"]
        try:
            specialization = Specialization.objects.get(category=name) # if the typed word matches exactly with the name of the specialization
            if specialization:
                return HttpResponseRedirect(reverse("categoryList", args=[name]))
        except Specialization.DoesNotExist:
            try:
                l1 = name.split()
                if len(l1)==3:
                    first_name = l1[1]
                    last_name = l1[2]
                    doctor = Doctor.objects.get(user__first_name=first_name, user__last_name=last_name) # if the word matches with the doctor name
                    if doctor:
                        return HttpResponseRedirect(reverse("checkDocProfile", args=[doctor.user.id]))
                else:
                    spl = Specialization.objects.filter(Q(category__icontains=name)) # else generate a list with results containing those set of letters if it exists
                    doc = Doctor.objects.filter(
                        Q(user__first_name__icontains=name) | Q(user__last_name__icontains=name))
                    return render(request, "getResult.html", context={'doctor': doc, 'specialization': spl, 'head_spl':head_spl,'head_doc':head_doc})
            except Doctor.DoesNotExist:
                spl = Specialization.objects.filter(Q(category__icontains=name))
                doc = Doctor.objects.filter(
                    Q(user__first_name__icontains=name) | Q(user__last_name__icontains=name))
                return render(request, "getResult.html", context={'doctor': doc, 'specialization': spl, 'head_spl':head_spl,'head_doc':head_doc})
    else:
        return render(request, "dump.html")

@login_required
def deletePicture(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return render(request, "dump.html")
    user.header_image.delete()
    user.save()
    if user.is_patient:
        return HttpResponseRedirect(reverse("updatePatProfile", args=[id]))
    else:
        return HttpResponseRedirect(reverse("updateAdmProfile", args=[id]))

@login_required
def documentUpload(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return render(request, "dump.html")
    try:
        patient = Patient.objects.get(user=user)
    except Patient.DoesNotExist:
        return render(request, "dump.html")
    if request.method == "POST":
        d = DocumentUpload.objects.create(patient=patient)
        d.p_name = request.POST["p_name"]
        d.document_name = request.POST["document_name"]
        d.document = request.FILES["document"]
        d.save()
        messages.error(request, "Your Document has been uploaded successfully!")

        return HttpResponseRedirect(reverse("documentUpload", args=[user.id]))
    else:
        form = DocumentUplaodForm()
        list = DocumentUpload.objects.filter(patient=patient)
        return render(request, "documentUpload.html", context={'form': form,'list':list, 'user':user,'head_spl':head_spl,'head_doc':head_doc})

def removeDocument(request, id):
    try:
        d = DocumentUpload.objects.get(pk=id)
    except DocumentUpload.DoesNotExist:
        return render(request, "dump.html")
    patient = d.patient
    return render(request, "askRemoveDocument.html", context={'d':d,'patient':patient})

def removeDocument1(request,id, patid):
    try:
        d = DocumentUpload.objects.get(pk=id)
    except DocumentUpload.DoesNotExist:
        return render(request, "dump.html")

    patient = Patient.objects.get(pk=patid)

    if patient == d.patient:
        d.document.delete()
        d.delete()
    return HttpResponseRedirect(reverse("documentUpload", args=[request.user.id]))
