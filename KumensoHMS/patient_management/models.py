import sys
import os
parent_dir = os.path.abspath("..")
sys.path.append(parent_dir)
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime, timezone
from django.dispatch import receiver
from django.db.models.signals import post_save



STATUS_CHOICES = [
        ("Checked in", "Checked in"),
        ("Collect Vitals", "Collect Vitals"),
        ("Perform diagnosis", "Perform diagnosis"),
        ("Prescription", "Prescription"),
        ("Complete", "Complete"),
    ]

GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other")
    ]

IDENTITY_TYPE_CHOICES = [
        ("nrc", "National Registration Card"),
        ("passport", "Passport")
    ]

TITLE_CHOICES = [
        ("mr.", "Mr."),
        ("mrs.", "Mrs."),
        ("miss", "Miss"),
        ("ms.", "Ms."),
        ("dr.", "Dr."),
        ("prof.", "Prof.")
    ]

# Create your models here.
class Patient(models.Model):
    """Represents the patient's personal information."""
    CIVIL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('separated', 'Separated'),
        ('domestic_partnership', 'Domestic Partnership')
    ]

    patient_id_number = models.CharField(max_length=50)
    #title = models.CharField(max_length=50, choices=TITLE_CHOICES)
    title_code = models.ForeignKey('users.UserTitle', on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    civil_status = models.ForeignKey('users.MaritalStatus', on_delete=models.CASCADE, blank=True, null=True)
    identity_type = models.CharField(max_length=30, choices=IDENTITY_TYPE_CHOICES, default="NRC")
    identity_number = models.CharField(max_length=50, unique=True)
    occupation = models.CharField(max_length=100)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name

class ContactInformation(models.Model):
    """Represents patient's contact information."""
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name="contact_info")
    email = models.EmailField(unique=True)
    phone_number_1 = models.CharField(max_length=20)
    phone_number_2 = models.CharField(max_length=20, blank=True, null=True)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=100)
    country = models.ForeignKey('users.Country', on_delete=models.CASCADE, blank=True, null=True)

class PrimaryContact(models.Model):
    """Represents the patient's primary contact."""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="primary_contact")
    title = models.ForeignKey('users.UserTitle', on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    relationship = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    identity_type = models.CharField(max_length=50, choices=IDENTITY_TYPE_CHOICES, default="nrc")
    identity_number = models.CharField(max_length=50, unique=True)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Zambia')

class HealthCondition(models.Model):
    """Represents a specific health condition."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name


class Diagnosis(models.Model):
    checkin = models.ForeignKey("CheckIn", on_delete=models.CASCADE,blank=True, null=True)
    date = models.DateTimeField(default=datetime.today)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.ForeignKey(HealthCondition, on_delete=models.CASCADE)

    remarks = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.patient}"
    


class Vitals(models.Model):
    checkin = models.ForeignKey("CheckIn", on_delete=models.CASCADE,blank=True, null=True)
    date = models.DateTimeField(default=datetime.today)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    pulseRate = models.IntegerField()
    temperature = models.IntegerField()
    height = models.IntegerField()
    bp = models.IntegerField()
    respiration = models.IntegerField()
    weight = models.IntegerField()
    def __str__(self):
        return f"{self.patient}"


class PatientHealthRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="patient_health_record")
    allergies = models.TextField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    surgical_history = models.TextField(blank=True, null=True)
    medication = models.TextField(blank=True, null=True)
    warnings = models.TextField(blank=True, null=True)
    social_history = models.TextField(blank=True, null=True)
    family_history = models.TextField(blank=True, null=True)
    personal_history = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.patient}"


class RiskFactors(models.Model):
    """Represents a patient's risk factors."""
    SMOKING_STATUS_CHOICES = [
        ('never', 'Never'),
        ('former', 'Former'),
        ('current', 'Current')
    ]

    ALCOHOL_USE_CHOICES = [
        ('never', 'Never'),
        ('occasional', 'Occasional'),
        ('regular', 'Regular')
    ]

    paiient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="risk_factors")
    health_conditions = models.CharField(max_length=100)
    smoking_status = models.CharField(max_length=20, choices=SMOKING_STATUS_CHOICES)
    smoking_status_description = models.TextField(blank=True, null=True)
    alcohol_use = models.CharField(max_length=20, choices=ALCOHOL_USE_CHOICES)
    alcohol_use_description = models.TextField(blank=True, null=True)




class AppointmentDateTime(models.Model):
    appointment_time = models.TimeField(unique=True)
    def __str__(self):
        return f"{self.appointment_time}"

class Appointments(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Checked-In', 'Checked-In'),
        ('PRN', 'PRN'),
        ('Reschedule', 'Reschedule'),
    ]
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE, blank=True, null=True)
    doctor = models.ForeignKey("users.MyUser", on_delete=models.CASCADE, blank=True, null=True)
    appointment_date = models.DateField(verbose_name='Date of Birth', blank=True, null=True)
    start_time = models.ForeignKey(AppointmentDateTime, on_delete=models.CASCADE, related_name="appointments_start")
    end_time = models.ForeignKey(AppointmentDateTime, on_delete=models.CASCADE, related_name="appointments_end")
    appointment_reason = models.TextField(max_length=100)
    scheduler = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Active")
    
  
    
    def clean(self):
        # Check for overlapping appointments
        if self.appointment_date and self.start_time and self.end_time:
            overlapping_appointments = Appointments.objects.filter(
                Q(appointment_date=self.appointment_date),
                (
                    Q(start_time__lt=self.end_time) &
                    Q(end_time__gt=self.start_time)
                )
            ).exclude(pk=self.pk)  # Exclude the current instance if editing
            if overlapping_appointments.exists():
                raise ValidationError("Another appointment exists within this time range.")
            
class Medicine_prescription(models.Model):
    checkin_record = models.ForeignKey("CheckIn", on_delete=models.CASCADE,blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,blank=True, null=True)
    prescribed_id = models.ForeignKey("users.inventory_List",on_delete=models.CASCADE,blank=True)
    days = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField()
    instruction = models.TextField(blank=True, null=True)
    advice = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2,blank=True, null=True)
    
    def __str__(self):
        return f"{self.checkin_record}"

class CheckIn(models.Model):
    checkin_date = models.DateTimeField(default=datetime.today)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    staff = models.ForeignKey("users.MyUser", on_delete=models.CASCADE,blank=True,limit_choices_to={'designation': '1'})
    checkout_date = models.DateTimeField(default=datetime.today)
    department = models.ForeignKey("users.Department", on_delete=models.CASCADE,blank=True,null=True)
    service = models.ManyToManyField("users.Services", blank=True)
    medication = models.ManyToManyField(Medicine_prescription, blank=True,related_name="checkins")
    checkin_id = models.AutoField(primary_key=True)
    #status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Checked in")
    status = models.ForeignKey('users.Status',on_delete=models.CASCADE, blank=True)
    def __str__(self):
        return f"{self.checkin_id}"

    def save(self, *args, **kwargs):
        if not self.checkin_id:  # Check if checkin_id is not set
            today = datetime.now(timezone.utc)
            formatted_date = today.strftime("%d%m%y")
            last_checkin = CheckIn.objects.order_by('-checkin_date').first()
            new_value = 1

            if last_checkin:
                last_id = last_checkin.checkin_id
                last_date = str(last_id)[:6]
                if last_date == formatted_date:
                    new_value = int(str(last_id)[6:]) + 1

            # Ensure the generated ID is unique
            while CheckIn.objects.filter(checkin_id=int(f"{formatted_date}{new_value:02d}")).exists():
                new_value += 1

            self.checkin_id = int(f"{formatted_date}{new_value:02d}")
        super().save(*args, **kwargs)


