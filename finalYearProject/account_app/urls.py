from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

urlpatterns = [
    path("PatientRegistration/", views.patient_registration, name="PatientRegistration"),
    path("DoctorRegistration/", views.doctor_registration, name="DoctorRegistration"),
    path("SignUp/", views.signUp, name="signUp"),
    path("PatientSignUp/", views.patient_signup, name="PatientSignUp"),
    path("DoctorSignUp/", views.doctor_signup, name="DoctorSignUp"),
    path("DoctorSignUp2/", views.doctor_signup2, name="DoctorSignUp2"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path('doLogin/', views.doLogin, name="doLogin"),
    path("", auth_views.LogoutView.as_view(), name="logout"),

    #path("reset/", views.reset_views, name="reset"),
    #path("reset2/", views.reset2_views, name="reset2"),

    #Reset Password Urls
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path("password_reset/done/",auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),name="password_reset_done"),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),name="password_reset_confirm"),
    path("reset/done/",auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),name="password_reset_complete"),

]