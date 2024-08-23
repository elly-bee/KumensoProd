from django.urls import path

from . import views

app_name = 'patient_app'
urlpatterns = [
    path("", views.attending_patient, name="patient_management_index",),
    path("listPatient", views.list_patient, name="listPatient",),
    path("attPatient", views.attending_patient, name="attPatient",),
    path("new_patient", views.new_patient, name="new_patient"),
    path("<int:patient_id>", views.patient_detail, name="patient_detail"),
    path("appointment", views.AppointmentSchedule.as_view(template_name = 'patient_management/appointment_form.html'), name="appointment"),
    path("appointmentlist", views.AppointmentSchedule.as_view(template_name = 'patient_management/appointment_list.html'), name="appointmentlist"),
    path("appointmentmanage/<int:pk>", views.AppointmentUpdateView.as_view(template_name = 'patient_management/appointment_manage.html'), name="appointmentmanage"),
    path("patientDetials/<int:pk>", views.PatientDetailsView.as_view(), name="patientDetials"),
    path("patientInvoice", views.invoiceList, name="patientInvoice"),
    path("patientInvoiceDetials/<int:pk>", views.PatientInvoiceView.as_view(), name="patientInvoiceDetials"),

    
    
    
]