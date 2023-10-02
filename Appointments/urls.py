from django.urls import path

from .views import *
# from Appointments.views import DoctorsListView
urlpatterns = [
    path('getDoctors/',getDoctors),
    path('getDoctors/<str:doctor_id>/', getDoctordetails, name='doctor-detail'),
    path('bookAppointment/',bookAppointment,name = "book-appointment"),
    path('addDoctor/',addDoctor),
    path('appointments/<str:doctor_id>/', doctor_appointments, name='doctor-appointments'),

]

