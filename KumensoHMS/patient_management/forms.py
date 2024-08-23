import sys
import os
parent_dir = os.path.abspath("..")
sys.path.append(parent_dir)
from users.models import Services
from django.utils import timezone
import datetime
from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

class AppointmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Appointments
        fields = ['patient', 'doctor', 'appointment_reason', 'start_time', 'end_time', 'status', 'appointment_date']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.Select(attrs={'type': 'date', 'class': 'form-control'}),
            'end_time': forms.Select(attrs={'type': 'date', 'class': 'form-control'}),
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'appointment_reason': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance



class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointments
        fields = ['patient', 'doctor', 'appointment_reason', 'start_time', 'end_time', 'status', 'appointment_date']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.Select(attrs={'type': 'date', 'class': 'form-control'}),
            'end_time': forms.Select(attrs={'type': 'date', 'class': 'form-control'}),
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'appointment_reason': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
            instance = super().save(commit=False)
            if commit:
                instance.save()
            return instance

    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get("appointment_date")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if appointment_date and start_time and end_time:
            if appointment_date <= datetime.now().date():
                self.add_error('appointment_date', _("Appointment date should be in the future."))
                return cleaned_data

            overlapping_appointments = Appointments.objects.filter(
                Q(appointment_date=appointment_date),
                (Q(start_time__lt=end_time) & Q(end_time__gt=start_time))
            ).exclude(pk=self.instance.pk if self.instance else None)

            if overlapping_appointments.exists():
                conflicting_appointment = overlapping_appointments.first()
                conflicting_date = conflicting_appointment.appointment_date
                conflicting_start_time = conflicting_appointment.start_time
                conflicting_end_time = conflicting_appointment.end_time
                conflicting_details = f"Date: {conflicting_date}, Time: {conflicting_start_time}-{conflicting_end_time}"
                self.add_error('appointment_date', _(f"Another appointment exists within this time range: {conflicting_details}."))


        return cleaned_data
        



class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ["patient_id_number", "registration_date"]
        widgets = {
            'title_code': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.TextInput(attrs={'type': 'date','class': 'form-control'}),
            'civil_status': forms.Select(attrs={'class': 'form-control'}),
            'identity_type': forms.Select(attrs={'class': 'form-control'}),
            'identity_number': forms.TextInput(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            "first_name": {
                "required": "Please enter your first name Mwelwa come on now.",
                "max_length": "Please enter a first name shorter than 50 characters."
            },
            "middle_name": {
                "max_length": "Please enter a middle name shorter than 50 characters."
            },
            "last_name": {
                "required": "Please enter your last name.",
                "max_length": "Please enter a last name shorter than 50 characters."
            },
            "date_of_birth": {
                "required": "Please enter your date of birth."
            },
            "gender": {
                "required": "Please select your gender."
            },
            "identity_type": {
                "required": "Please select your identity document type."
            },
            "identity_number": {
                "required": "Please enter your identity number.",
                "max_length": "Your identity number must not be longer than 50 characters.",
                "unique": "This identity number is already in use. Please enter a unique identity number."
            },
            "occupation": {
                "required": "Please enter the occupation.",
                "max_length": "Occupation cannot exceed 50 characters.",
            },
        }

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInformation
        fields = '__all__'
        exclude = ["patient"]
       


class PrimaryContactForm(forms.ModelForm):
    class Meta:
        model = PrimaryContact
        exclude = ["patient"]

class HealthConditionForm(forms.ModelForm):
    class Meta:
        model = HealthCondition
        fields = "__all__"

class PatientHealthRecordForm(forms.ModelForm):
    class Meta:
        model = PatientHealthRecord
        fields = ['allergies', 'medical_history', 'surgical_history', 'medication', 'warnings','social_history','family_history','personal_history']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control', 'rows': '2'}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            'surgical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            'medication': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            'warnings': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            'social_history': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            'family_history': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            'personal_history': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            
            
        }

class RiskFactorsForm(forms.ModelForm):
    class Meta:
        model = RiskFactors
        exclude = ["patient"]

class VitalsForm(forms.ModelForm):
    class Meta:
        model = Vitals
        #exclude = ["patient"]
        fields = ['pulseRate', 'temperature', 'height', 'bp', 'respiration', 'weight']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'pulseRate': forms.TextInput(attrs={'class': 'form-control'}),
            'temperature': forms.TextInput(attrs={'class': 'form-control'}),
            'height': forms.TextInput(attrs={'class': 'form-control'}),
            'bp': forms.TextInput(attrs={'class': 'form-control'}),
            'respiration': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['diagnosis', 'remarks']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'diagnosis': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CheckInForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CheckInForm, self).__init__(*args, **kwargs)
        self.fields['service'].queryset = Services.objects.all()
    class Meta:
        model = CheckIn
        fields = ['patient','staff','department','status','service','medication']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'staff': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'medication': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        }

class CheckInUpdate(forms.ModelForm):
    class Meta:
        model = CheckIn
        fields = ['status',]
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'staff': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'medication': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        }


class Prescription_form(forms.ModelForm):
    class Meta:
        model = Medicine_prescription
        fields = ['prescribed_id', 'days', 'quantity', 'instruction', 'advice','checkin_record']
        widgets = {
            'checkin_record': forms.Select(attrs={'class': 'form-control'}),
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'prescribed_id': forms.Select(attrs={'class': 'form-control'}),
            'days': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'instruction': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            'advice': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
        }