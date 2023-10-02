from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db import IntegrityError
# Create your views here.

# class DoctorsListView(APIView):
#     def get(self,request):
#         queryset = Doctors.objects.all()
#         print(queryset)
#         serializerclass = DoctorSerializer(queryset,many= True)
#         try:
#             print(serializerclass.data)
#             return Response(serializerclass.data)
        
#         except Exception as e:
#             print(e)
#             return Response(serializerclass.error_messages)

@api_view(['GET'])
def getDoctors(request):
    data = Doctors.objects.all()
    serialized = DoctorSerializer(data,many = True)
    return Response(serialized.data)

@api_view(['GET'])
def getDoctordetails(request,doctor_id):
    try:
        data = Doctors.objects.get(id = doctor_id)    
    except Exception as E:
        return Response({'error': 'Doctor not found'},status=status.HTTP_400_BAD_REQUEST)

    serializedData = DocSerializer(data)
    return Response(serializedData.data,status=status.HTTP_200_OK)


@api_view(['POST'])
def bookAppointment(request):
    serializer = AppointmentSerializer(data = request.data)
    if serializer.is_valid():
        doctor = serializer.validated_data['doctor']
        patient_name = serializer.validated_data['patient_name']
        appointment_time = serializer.validated_data['appointment_time']
        weekly_schedule = serializer.validated_data['weekly_schedule']

        existing_appointment = Appointment.objects.filter(
            doctor=doctor,
            appointment_time=appointment_time,
            weekly_schedule=weekly_schedule,

        ).first()
            
        if existing_appointment:
            return Response({'error':
                             'Appointment slot already booked'},status = status.HTTP_400_BAD_REQUEST)
        
        appointment = Appointment(
            doctor = doctor,
            patient_name = patient_name,
            appointment_time = appointment_time,
            weekly_schedule = weekly_schedule,
            status = 'confirmed'
        )
        try:
            appointment.save()

        except IntegrityError:
            return Response({'error':'slot booked by another user'},status = status.HTTP_400_BAD_REQUEST)
        
        return Response({'message':'Appointment booked successfully'},status = status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
def addDoctor(request):
    serializer = DocSerializer(data = request.data)
    if serializer.is_valid():
        Doctors = serializer.save()
        return Response({'message':'post created','id' :Doctors.id},status = status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def doctor_appointments(request, doctor_id):
    
    appointments = Appointment.objects.filter(doctor_id=doctor_id)
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)
