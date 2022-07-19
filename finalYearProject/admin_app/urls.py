from django.urls import path
from . import views
from .views import addCategory
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.adminHome,name="adminHome"),
    path("AdminRegistration/", views.admin_registration, name="AdminRegistration"),
    path("AdminRegistration2/", views.admin_registration2, name="AdminRegistration2"),
    path('updateAdmProfile/<int:id>/',views.updateAdmProfile,name="updateAdmProfile"),
    path('viewAdmProfile/<int:id>/',views.viewAdmProfile,name="viewAdmProfile"),
    path('addCategory/',views.addCategory,name="addCategory"),
    path('updateCategory/<int:id>/',views.updateCategory,name="updateCategory"),
    path('catList/',views.catList,name="catList"),
    path('admList/',views.admList,name="admList"),
    path('updateList/',views.updateList,name="updateList"),
    path('docList/<str:cat>/',views.docList,name="docList"),
    path('ratings/<int:id>',views.ratings,name="ratings"),
    path('banDoc/<int:id>',views.banDoc,name="banDoc"),
    path('adminSearch/',views.adminSearch,name="adminSearch"),
    path('deleteAdmin/<int:id>',views.deleteAdmin,name="deleteAdmin"),
]