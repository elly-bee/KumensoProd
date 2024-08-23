from django.contrib import admin
import sys
import os
parent_dir = os.path.abspath("..")

# Print the parent directory path
print(parent_dir)

# Append the parent directory to sys.path
sys.path.append(parent_dir)

# Now you can import the Patient model from the patient_management package
from patient_management.models import *
#from ..patient_management.models import Patient,PatientHealthRecord,PrimaryContact
from .models import *



# Register your models here.
"""class UserAdmin(admin.ModelAdmin):
    #list_display = ('first_name', 'last_name', 'email', 'city', 'user_type')
    list_filter = ('city', 'user_type')
    search_fields = ('first_name', 'last_name', 'username', 'city')"""

admin.site.register(MyUser)
admin.site.register(UserTitle)
admin.site.register(UserRoles)
admin.site.register(MaritalStatus)
admin.site.register(UserDesignation)
admin.site.register(Department)
admin.site.register(Company)
admin.site.register(Country)
admin.site.register(Profile)
admin.site.register(Gender)
admin.site.register(Patient)
admin.site.register(PatientHealthRecord)
admin.site.register(PrimaryContact)
admin.site.register(Appointments)
admin.site.register(AppointmentDateTime)
admin.site.register(ContactInformation)
admin.site.register(Vitals)
admin.site.register(Diagnosis)
admin.site.register(HealthCondition)
admin.site.register(Revenue)
admin.site.register(Inventory)
admin.site.register(GeneralExpenses)
admin.site.register(Expenses)
admin.site.register(inventory_List)
admin.site.register(Medicine_Category)
admin.site.register(Medicine)
admin.site.register(Services_Category)
admin.site.register(Services)
admin.site.register(Medicine_prescription)
admin.site.register(CheckIn)
admin.site.register(Status)















