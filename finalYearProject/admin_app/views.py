from django.shortcuts import render, redirect
from .forms import AddCategoryForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Specialization, BannedUser
from account_app.models import Doctor, User, Admin
from account_app.forms import AdminRegistrationForm
from patient_app.models import Reviews
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.utils.datastructures import MultiValueDictKeyError
import os
from django.db.models import Q
# Create your views here.

head_spl = Specialization.objects.all()
head_doc = Doctor.objects.all()

@login_required
def adminHome(request):
        return render(request,"adminHome.html", context = {'head_doc':head_doc,'head_spl':head_spl})

def admin_registration(request):
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST['username'])
            if user:
                messages.error(request, "User has an account already")
                return redirect('AdminRegistration')
        except User.DoesNotExist:
            request.session["username"]=request.POST['username']
            if request.POST['password1'] == request.POST['password2']:
                request.session["email"] = request.POST['email']
                request.session["password"] = request.POST['password1']
                return HttpResponseRedirect(reverse('AdminRegistration2'))
            else:
                messages.error(request, "Password Mismatch!")
                return HttpResponseRedirect(reverse('AdminRegistration'))
    else:
        form = AdminRegistrationForm()
        return render(request, 'admin_registration.html', {'form': form, 'head_doc':head_doc,'head_spl':head_spl})


def admin_registration2(request):
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
        user.is_admin = True
        user.is_superuser = True
        user.save()
        admin = Admin.objects.create(user=user)
        admin.save()
        messages.success(request, ("User Created Successfully!"))
        return redirect('AdminRegistration')
    else:
        form = AdminRegistrationForm()
        return render(request, 'admin_registration2.html', {'form': form, 'head_doc':head_doc,'head_spl':head_spl})

@login_required
def updateAdmProfile(request, id):
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
        admin = Admin.objects.get(user=user)
        admin.save()
        messages.error(request, "Your Profile Details have been successfully updated!")
        return HttpResponseRedirect(reverse('viewAdmProfile', args=[id]))
    else:
        return render(request, 'updateAdmProfile.html', context={'user': user, 'head_doc':head_doc,'head_spl':head_spl})

@login_required
def viewAdmProfile(request, id):
    try:
        admin = Admin.objects.get(pk=id)
    except Admin.DoesNotExist:
        return render(request, "dump.html") #dump end
    age = admin.user.calculateAge()
    return render(request, 'viewAdmProfile.html', context={'admin': admin,'age':age, 'head_doc':head_doc,'head_spl':head_spl})


@login_required
def addCategory(request):
    if request.method == "POST":
        form = AddCategoryForm(request.POST, request.FILES) # request.FILES is necessary so that the images can be
        if form.is_valid():                                 # saved in the backend
            form.save()
            messages.success(request, ("Category added successfully!"))
            return redirect('addCategory')
    else:
        form = AddCategoryForm()
        return render(request, 'addCategory.html', context={'form':form,'head_doc':head_doc,'head_spl':head_spl})

@login_required
def updateList(request):
    specialization = Specialization.objects.all().order_by("category")
    paginator = Paginator(specialization, 8)  # to add paging to the website
    count = specialization.count()
    page = request.GET.get('pg')
    all_specialization = paginator.get_page(page)
    return render(request, "updateList.html", context={'specialization': all_specialization,'count':count ,'head_doc':head_doc,'head_spl':head_spl})

@login_required
def catList(request):
    specialization = Specialization.objects.all().order_by("category")
    paginator = Paginator(specialization, 8)  # to add paging to the website
    count = specialization.count()
    page = request.GET.get('pg')
    all_specialization = paginator.get_page(page)
    return render(request, "catList.html", context={'specialization': all_specialization, 'count': count,'head_doc':head_doc,'head_spl':head_spl})

@login_required
def admList(request):
    admin = Admin.objects.all()
    paginator = Paginator(admin, 6)  # to add paging to the website
    count = admin.count()
    page = request.GET.get('pg')
    all_admin = paginator.get_page(page)
    return render(request, "admList.html", context={'admin': all_admin, 'count': count,'head_doc':head_doc,'head_spl':head_spl})


@login_required
def updateCategory(request, id):
        try:
            specialization = Specialization.objects.get(pk=id)
        except Specialization.DoesNotExist:
            return render(request, "dump.html")
        image = specialization.header_image
        if request.method == "POST":
            specialization.category = request.POST["category"]
            try:
                if request.FILES["header_image"]:
                    if image:
                        if os.path.exists(image.path):  # to remove the image source and replace it with the new image
                            os.remove(image.path)
                    specialization.header_image = request.FILES["header_image"]
            except MultiValueDictKeyError:
                if image:
                    specialization.header_image = image
            specialization.save()
            messages.error(request, "Category has been updated successfully!")
            return redirect("updateList")
        else:
            return render(request, "updateCategory.html", context={'spl': specialization,'head_doc':head_doc,'head_spl':head_spl})

@login_required
def docList(request, cat):
    doctor = Doctor.objects.filter(specialization=cat).order_by("user__first_name")
    count = doctor.count()
    paginator = Paginator(doctor, 6)  # to add paging to the website
    page = request.GET.get('pg')
    all_doctor = paginator.get_page(page)
    return render(request, "docList.html", {'doctor': all_doctor, 'count': count, 'head_doc':head_doc,'head_spl':head_spl})

@login_required
def ratings(request, id):
    user = User.objects.get(pk=id)
    try:
        doctor = Doctor.objects.get(user=user)
    except Doctor.DoesNotExist:
        return render(request, "dump.html")
    reviews = Reviews.objects.filter(doctor=doctor)
    count = reviews.count()
    return render(request, "ratings.html", context={'doctor':doctor,'reviews':reviews,'count':count,'head_doc':head_doc,'head_spl':head_spl})

@login_required
def banDoc(request, id): # a function to ban a doctor with a unique doctor reg_id and delete their instance where ever present
    user = User.objects.get(pk=id)
    try:
        doctor = Doctor.objects.get(user=user)
    except Doctor.DoesNotExist:
        return render(request, "dump.html")
    bannedDoc = BannedUser.objects.create(userid=doctor.doctor_reg_id)
    bannedDoc.save()
    doctor.delete()
    return redirect("catList")

def adminSearch(request):
    if request.method == "POST":
        name = request.POST["tags"]
        try:
            specialization = Specialization.objects.get(category=name)  # if the typed word matches exactly with the name of the specialization
            if specialization:
                return HttpResponseRedirect(reverse("docList", args=[name]))
        except Specialization.DoesNotExist:
            try:
                l1 = name.split()
                if len(l1) == 3:
                    first_name = l1[1]
                    last_name = l1[2]
                    doctor = Doctor.objects.get(user__first_name=first_name,
                                                user__last_name=last_name)  # if the word matches with the doctor name
                    if doctor:
                        return HttpResponseRedirect(reverse("ratings", args=[doctor.user.id]))
                else:
                    spl = Specialization.objects.filter(
                        Q(category__icontains=name))  # else generate a list with results containing those set of letters if it exists
                    doc = Doctor.objects.filter(
                        Q(user__first_name__icontains=name) | Q(user__last_name__icontains=name))
                    return render(request, "adminSearch.html",
                                  context={'doctor': doc, 'specialization': spl, 'head_spl': head_spl,
                                           'head_doc': head_doc})
            except Doctor.DoesNotExist:
                spl = Specialization.objects.filter(Q(category__icontains=name))
                doc = Doctor.objects.filter(
                    Q(user__first_name__icontains=name) | Q(user__last_name__icontains=name))
                return render(request, "adminSearch.html",
                              context={'doctor': doc, 'specialization': spl, 'head_spl': head_spl,
                                       'head_doc': head_doc})
    else:
        return render(request, "dump.html")


def deleteAdmin(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return render(request, "dump.html")
    user.delete()
    return redirect('admList')
