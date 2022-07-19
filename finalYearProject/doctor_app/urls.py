from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('<int:id>/',views.doctorHome,name="doctorHome"),
    path('updateDocProfile/<int:id>/',views.updateDocProfile,name="updateDocProfile"),
    path('viewDocProfile/<int:id>/',views.viewDocProfile,name="viewDocProfile"),
    path('docHistoryApp/<int:id>/',views.docHistoryApp,name="docHistoryApp"),
    path('docCancelledApp/<int:id>/',views.docCancelledApp,name="docCancelledApp"),
    path('docUpcomingApp/<int:id>/',views.docUpcomingApp,name="docUpcomingApp"),
    path('docReviews/<int:id>/',views.docReviews,name="docReviews"),
    path('cancelAppointment/<int:id>/',views.cancelAppointment,name="cancelAppointment"),
    path('cancelAppointment1/<int:id>/',views.cancelAppointment1,name="cancelAppointment1"),
    path('doneAppointment/<int:id>/',views.doneAppointment,name="doneAppointment"),
    path('viewPdf/<int:id>/',views.viewPdf,name="viewPdf"),
]