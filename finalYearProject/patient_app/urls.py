from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.patientHome,name="patientHome"),
    path('updatePatProfile/<int:id>/',views.updatePatProfile,name="updatePatProfile"),
    path('viewPatProfile/<int:id>/',views.viewPatProfile,name="viewPatProfile"),
    path('category/<str:cat>/',views.categoryList,name="categoryList"),
    path('specializationList/',views.specializationList,name="specializationList"),
    path('checkDocProfile/<int:id>/',views.checkDocProfile,name="checkDocProfile"),
    path('bookAppointment/<int:id>/<int:patid>/',views.bookAppointment,name="bookAppointment"),
    path('patientInfo/',views.patientInfo,name="patientInfo"),
    path('currentApp/<int:id>/',views.currentApp,name="currentApp"),
    path('patCancelAppointment/<int:id>/',views.patCancelAppointment,name="patCancelAppointment"),
    path('patCancelAppointment1/<int:id>/',views.patCancelAppointment1,name="patCancelAppointment1"),
    path('historyApp/<int:id>/',views.historyApp,name="historyApp"),
    path('cancelledApp/<int:id>/',views.cancelledApp,name="cancelledApp"),
    path('likeDoc/<int:id>/<int:patid>/',views.likeDoc,name="likeDoc"),
    path('dislikeDoc/<int:id>/<int:patid>/',views.dislikeDoc,name="dislikeDoc"),
    path('giveReview/<int:id>/',views.giveReview,name="giveReview"),
    path('getResult/',views.getResult,name="getResult"),
    path('deletePicture/<int:id>/',views.deletePicture,name="deletePicture"),
    path('documentUpload/<int:id>/',views.documentUpload,name="documentUpload"),
    path('removeDocument/<int:id>/',views.removeDocument,name="removeDocument"),
    path('removeDocument1/<int:id>/<int:patid>/',views.removeDocument1,name="removeDocument1"),
]