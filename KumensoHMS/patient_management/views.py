import sys
import os
parent_dir = os.path.abspath("..")

import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.forms import inlineformset_factory, formset_factory
from formtools.wizard.views import SessionWizardView # type: ignore
from django.views.generic import ListView,FormView,CreateView,UpdateView,View
from django.urls import reverse_lazy
from .forms import *
from .models import Patient as PatientModel
from .models import ContactInformation,Vitals
from .models import PrimaryContact as PrimaryContactModel
from .models import PatientHealthRecord as PatientHealthRecordModel
from .models import RiskFactors as RiskFactorsModel
from .models import Appointments
from datetime import datetime, time
from .models import AppointmentDateTime
#from .appointment import generate_time_blocks
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from users.models import inventory_List,Inventory,MyUser
from decimal import Decimal, ROUND_HALF_UP
from users.models import Company
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import OuterRef, Subquery


def list_patient(request):
    user = request.user
    userID = MyUser.objects.get(username=user)
    patients = PatientModel.objects.prefetch_related("contact_info").all()
    checkin = CheckIn.objects.all()
    latest_checkin_subquery = CheckIn.objects.filter(
        patient=OuterRef('patient')
    ).order_by('-checkin_date').values('checkin_id')[:1]
    patient_checkin = CheckIn.objects.filter(
        checkin_id__in=Subquery(latest_checkin_subquery)
    ).values(
        'patient__id',
        'patient__first_name',
        'patient__middle_name',
        'patient__last_name',
        'patient__gender',
        'patient__date_of_birth',
        'patient__civil_status__name',
        'patient__identity_number',
        'patient__identity_type',
        'patient__occupation',
        'patient__registration_date',
        'department__name',
        'status',
        'staff__first_name',
        'staff__last_name',
        'staff__title_code__title_name',
        'staff__department__name',
        'staff__designation__name',
        'staff__user_roles__role_name',
        'checkin_date'
    )
    #patient_checkin = patient_checkin.filter(department__name = userID.department)
    context = {
        "patients": patients,
        "checkIn": checkin,
        'patient_checkin':patient_checkin
    }
    return render(request, "patient_management/patient_list.html", context)

def attending_patient(request):
    user = request.user
    userID = MyUser.objects.get(username=user)
    patients = PatientModel.objects.prefetch_related("contact_info").all()
    checkin = CheckIn.objects.all()
    latest_checkin_subquery = CheckIn.objects.filter(
        patient=OuterRef('patient')
    ).order_by('-checkin_date').values('checkin_id')[:1]
    patient_checkin = CheckIn.objects.filter(
        checkin_id__in=Subquery(latest_checkin_subquery)
    ).values(
        'patient__id',
        'patient__first_name',
        'patient__middle_name',
        'patient__last_name',
        'patient__gender',
        'patient__date_of_birth',
        'patient__civil_status__name',
        'patient__identity_number',
        'patient__identity_type',
        'patient__occupation',
        'patient__registration_date',
        'department__name',
        'status',
        'staff__first_name',
        'staff__last_name',
        'staff__title_code__title_name',
        'staff__department__name',
        'staff__designation__name',
        'staff__user_roles__role_name',
        'checkin_date'
    )
    #patient_checkin = patient_checkin.filter(department__name = userID.department,status='Perform diagnosis' )
    context = {
        "patients": patients,
        "checkIn": checkin,
        'patient_checkin':patient_checkin
    }
    return render(request, "patient_management/index.html", context)

def new_patient(request):
    ContactInfoFormSet = inlineformset_factory(PatientModel, ContactInformation, form=ContactInfoForm, extra=1)
    PrimaryContactFormSet = inlineformset_factory(PatientModel, PrimaryContactModel, form=PrimaryContactForm, extra=1)
    PatientHealthRecordFormSet = inlineformset_factory(PatientModel, PatientHealthRecordModel, form=PatientHealthRecordForm, extra=1)
    RiskFactorsFormSet = inlineformset_factory(PatientModel, RiskFactorsModel, form=RiskFactorsForm, extra=1)

    if request.method == "POST":
        patient_form = PatientForm(request.POST)
        contact_formset = ContactInfoFormSet(request.POST, instance=PatientModel())
        primary_contact_formset = PrimaryContactFormSet(request.POST, instance=PatientModel())
        health_record_formset = PatientHealthRecordFormSet(request.POST, instance=PatientModel())
        risk_factors_formset = RiskFactorsFormSet(request.POST, instance=PatientModel())

        forms_valid = all([
            patient_form.is_valid(),
            contact_formset.is_valid(),
            primary_contact_formset.is_valid(),
            health_record_formset.is_valid(),
            risk_factors_formset.is_valid()
        ])

        # Ensure each form within the formsets is also individually valid
        for formset in [contact_formset, primary_contact_formset, health_record_formset, risk_factors_formset]:
            for form in formset:
                if not form.is_valid():
                    forms_valid = False

        if forms_valid:
            patient_instance = patient_form.save()
            contact_instances = contact_formset.save(commit=False)
            primary_contact_instances = primary_contact_formset.save(commit=False)
            health_record_instances = health_record_formset.save(commit=False)
            risk_factors_instances = risk_factors_formset.save(commit=False)

            for contact_instance in contact_instances:
                contact_instance.patient = patient_instance
                contact_instance.save()

            for primary_contact_instance in primary_contact_instances:
                primary_contact_instance.patient = patient_instance
                primary_contact_instance.save()

            for health_record_instance in health_record_instances:
                health_record_instance.patient = patient_instance
                health_record_instance.save()

            for risk_factors_instance in risk_factors_instances:
                risk_factors_instance.patient = patient_instance
                risk_factors_instance.save()

            return redirect(reverse("patient_app:patient_management_index"))

    else:
        patient_form = PatientForm()
        contact_formset = ContactInfoFormSet()
        primary_contact_formset = PrimaryContactFormSet()
        health_record_formset = PatientHealthRecordFormSet()
        risk_factors_formset = RiskFactorsFormSet()

    return render(request, "patient_management/new_patient.html", {
        "patient_form": patient_form,
        "contact_formset": contact_formset,
        "primary_contact_formset": primary_contact_formset,
        "health_record_formset": health_record_formset,
        "risk_factors_formset": risk_factors_formset,
    })

def patient_detail(request):
    pass

@method_decorator(login_required, name='dispatch')
class AppointmentSchedule(CreateView):
    model = Appointments
    
    success_url = reverse_lazy('user_app:dashboard')
    form_class = AppointmentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Appointmentdata'] = {
            'Appointment': Appointments.objects.all(),
            'activeApp': Appointments.objects.filter(status='Active')
        }
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class AppointmentUpdateView(UpdateView):

    model = Appointments
    form_class = AppointmentUpdateForm
    template_name = 'patient_management/appointment_manage.html'
    success_url = reverse_lazy('patient_app:appointmentlist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['Appointmentdata'] = {
            'Appointment': Appointments.objects.all(),
            'activeApp': Appointments.objects.filter(id=pk)
        }
        return context

    def form_valid(self, form):
        appointment_instance = self.get_object()  # Get the existing instance
        form.instance = appointment_instance  # Associate the form instance with the existing object
        appointment_instance = form.save()  # Save the changes to the appointment
        messages.success(self.request, "Appointment updated successfully!")
        return redirect(self.success_url)

@method_decorator(login_required, name='dispatch')
class PatientUpdate(UpdateView):
    model = PatientModel
    form_class = PatientForm
    template_name = 'patient_management/modelForms.html'
    success_url = reverse_lazy('patient_app:patient_management_index')

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        # Retrieve the patient instance using the primary key
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            return get_object_or_404(queryset, pk=pk)
        return None

    def get_form(self, form_class=None):
        # Override get_form to pass instance to the form
        patient_form = super().get_form(form_class)
        patient_form.instance = self.get_object()
        return patient_form 

    def form_valid(self, patient_form):
        # Save the form with the updated data
        self.object = patient_form.save()
        return super().form_valid(patient_form)

@method_decorator(login_required, name='dispatch')
class PatientDetailsView(PatientUpdate):
    template_name = 'patient_management/patient_details.html'
    

    def get(self, request, pk, *args, **kwargs):
        patient_instance = PatientModel.objects.get(pk=pk)
        # Call the get method of the parent class to get the form
        patient_form = self.get_form()
        patient_form = PatientForm(initial={
            'title_code': patient_instance.title_code,
            'first_name': patient_instance.first_name,
            'middle_name': patient_instance.middle_name,
            'last_name': patient_instance.last_name,
            'gender': patient_instance.gender,
            'date_of_birth': patient_instance.date_of_birth,
            'civil_status': patient_instance.civil_status,
            'identity_number': patient_instance.identity_number,
            'occupation': patient_instance.occupation,
            })
        
        try:
            patienthistory = PatientHealthRecord.objects.get(patient=patient_instance)
        except PatientHealthRecord.DoesNotExist:
            patient_health_record_form = PatientHealthRecordForm()
        else:
            patient_health_record_form = PatientHealthRecordForm(
                initial={
                    'patient': patient_instance,
                    'allergies': patienthistory.allergies,
                    'medical_history': patienthistory.medical_history,
                    'surgical_history': patienthistory.surgical_history,
                    'medication': patienthistory.medication,
                    'warnings': patienthistory.warnings,
                    'social_history': patienthistory.social_history,
                    'family_history': patienthistory.family_history,
                    'personal_history': patienthistory.personal_history,
                }
            )
        
        # Retrieve other necessary data
        vitals_instance = Vitals.objects.filter(patient=pk)
        diagnosis_instance = Diagnosis.objects.filter(patient=pk)
        contact_info_instance = ContactInformation.objects.filter(patient=pk).first()
        checkIn_instance = CheckIn.objects.filter(patient=patient_instance).last()
        medhistory = PatientHealthRecord.objects.filter(patient=patient_instance).values()
        patient = Patient.objects.all().values()

        try:
            checkin_instancein = CheckIn.objects.filter(checkin_id=checkIn_instance.checkin_id).prefetch_related('service', 'medication').first()
            if not checkin_instancein:
                checkin_instancein = None  # Set checkin_instancein to None when no results are found
        except Exception as e:
            print('Error occurred:', e)
            checkin_instancein = None  # Set checkin_instancein to None in case of any exception

        if checkin_instancein is not None:
            # Do something with checkin_instancein here
            # For example, uncomment the following line if you need to access services
            services = checkin_instancein.service.all().values()
            
        else:
            # Handle case where checkin_instancein is None (i.e., no results found)
            print('No CheckIn instance found.')

        medication = Medicine_prescription.objects.filter(checkin_record_id=checkIn_instance).values(
            'prescribed_id__Inventory_code',
            'prescribed_id__desc',
            'prescribed_id__selling_price')
        #medications = checkin_instancein.medication.filter(checkin_record=checkin_instancein)
        #print('_____',medication,'_____',services)
        
        
        checkInDetails = None
        try:
            checkUpdate = CheckIn.objects.filter(checkin_id=checkIn_instance.checkin_id).values('prescribed_id__desc','days','quantity','instruction','advice',)
            if checkUpdate.exists():
                checkInDetails = Medicine_prescription.objects.filter(checkin_record_id=checkIn_instance).values('prescribed_id__desc','days','quantity','instruction','advice',)
                #print(checkInDetails)
        except Exception as e:
            print("no record:", e)
        
        else:
            checkInDetails = Medicine_prescription.objects.filter(checkin_record_id=checkIn_instance).values('prescribed_id__desc','days','quantity','instruction','advice',)
        
        
        checkIn_ins = CheckIn.objects.filter(patient=patient_instance)
        # Create other form instances and populate them with existing data
        contact_info_form = ContactInfoForm(instance=contact_info_instance)
        primary_contact_form = PrimaryContactForm()
        health_condition_form = HealthConditionForm()
        risk_factors_form = RiskFactorsForm()
            # Group and arrange the services
        service_groups = []
        all_services = Services.objects.all()

        # Assuming you have a field 'group' in your Services model to indicate the group
        group_names = set(service.name for service in all_services)
       
        
        for group_name in group_names:
            group_services = all_services.filter(name=group_name)
            service_groups.append({'name': group_name, 'services': group_services})

  
        # Pass form instances to the template
        return render(request, self.template_name, {
            'checkIn': checkIn_instance,
            'patient_details': patient_instance,
            'patient': patient,
            'patient_form': patient_form,  # Use the form retrieved from PatientUpdate
            'contact_info_form': contact_info_form,
            'primary_contact_form': primary_contact_form,
            'health_condition_form': health_condition_form,
            'patient_health_record_form': patient_health_record_form,
            'risk_factors_form': risk_factors_form,
            'vitals_details': vitals_instance,
            'prescription_form': Prescription_form(initial={'patient': patient_instance,'checkin_record': checkIn_instance}),
            'checkIn_form': CheckInForm(initial={'patient': patient_instance,'staff':request.user}),
            'checkIn_status': CheckInUpdate(instance=checkIn_instance), #'staff':request.user,'department':staff_instance.department
            'vitals_form': VitalsForm(initial={'patient': patient_instance}),
            'diagnosis_form': DiagnosisForm(initial={'patient': patient_instance}),
            'diagnosis_details': diagnosis_instance,
            'service_groups': service_groups,
            'checkInDetails': checkInDetails,
            'medication': medication,
            'medhistory':medhistory        
        })
    
    def post(self, request, pk, *args, **kwargs):
        # Retrieve instances
        patient_instance = self.get_object()
        checkIn_instance = CheckIn.objects.filter(patient=patient_instance).last()
        contact_info_instance = ContactInformation.objects.filter(patient=pk).first()
        
        # Initialize forms
        patient_form = self.get_form()
        contact_info_form = ContactInfoForm(request.POST, instance=contact_info_instance)
        primary_contact_form = PrimaryContactForm(request.POST)
        health_condition_form = HealthConditionForm(request.POST)
        risk_factors_form = RiskFactorsForm(request.POST)
        diagnosis_form = DiagnosisForm(request.POST)
        checkIn_form = CheckInForm(request.POST, initial={'patient': patient_instance, 'staff': request.user})
        checkIn_update = CheckInUpdate(request.POST, instance=checkIn_instance, initial={'patient': patient_instance})
        prescription_form = Prescription_form(request.POST, initial={'patient': patient_instance, 'checkin_record': checkIn_instance})
        vitals_form = VitalsForm(request.POST)
        
        # Validate forms
        patient_form_is_valid = patient_form.is_valid()
        contact_info_form_is_valid = contact_info_form.is_valid()
        primary_contact_form_is_valid = primary_contact_form.is_valid()
        health_condition_form_is_valid = health_condition_form.is_valid()
        risk_factors_form_is_valid = risk_factors_form.is_valid()
        diagnosis_form_is_valid = diagnosis_form.is_valid()
        checkIn_form_is_valid = checkIn_form.is_valid()
        
        prescription_form_is_valid = prescription_form.is_valid()
        vitals_form_is_valid = vitals_form.is_valid()

        # Save valid forms
        try:
            checkIn_status_update = checkIn_update.is_valid()
            if checkIn_status_update:
                checkIn_update.save()
                messages.success(request, f'Key Bonus updated successfully for user')
        except Exception as e:
            pass


        if patient_form_is_valid:
            patient_form.save()

        if contact_info_form_is_valid:
            contact_info_form.save()

        if primary_contact_form_is_valid:
            primary_contact_form.save()

        if health_condition_form_is_valid:
            health_condition_form.save()

        if risk_factors_form_is_valid:
            risk_factors_form.save()

        if diagnosis_form_is_valid:
            diagnosis_instance = diagnosis_form.save(commit=False)
            diagnosis_instance.patient = patient_instance
            diagnosis_instance.save()

        if checkIn_form_is_valid:
            check_instance = checkIn_form.save(commit=False)
            check_instance.patient = patient_instance
            check_instance.staff = request.user
            check_instance.save()
            selected_services = request.POST.getlist('service')
            check_instance.service.set(selected_services)

        if prescription_form_is_valid:
            prescription_instance = prescription_form.save(commit=False)
            prescription_instance.patient = patient_instance
            prescription_instance.checkin_record = checkIn_instance
            prescription_instance.save()

        if vitals_form_is_valid:
            vitals_instance = vitals_form.save(commit=False)
            vitals_instance.patient = patient_instance
            vitals_instance.checkin = checkIn_instance
            vitals_instance.save()
            messages.success(request, f'Key Bonus updated successfully for user "{patient_instance}".')

        # Handle PatientHealthRecordForm
        try:
            patient_health_record_instance = PatientHealthRecord.objects.get(patient=patient_instance)
        except PatientHealthRecord.DoesNotExist:
            patient_health_record_instance = PatientHealthRecord(patient=patient_instance)

        patient_health_record_form = PatientHealthRecordForm(instance=patient_health_record_instance)
        if request.method == 'POST':
            patient_health_record_form = PatientHealthRecordForm(request.POST, instance=patient_health_record_instance)
            if patient_health_record_form.is_valid():
                patient_health_record_form.save()
        return redirect(reverse('patient_app:patientDetials', kwargs={'pk': pk}))
        #return messages.success(request, f'Key Bonus updated successfully for user "".')
 
def invoiceList(request):
    checkin = CheckIn.objects.prefetch_related('PatientModel').values(
        'checkin_date',
        'patient__first_name',
        'patient__last_name',
        # Add other fields from the Patient model as needed
        'staff_id',
        'checkout_date',
        'department_id',
        'checkin_id',
        'status',
    )
    context = {
        "checkIn": checkin
    }
    return render(request, "patient_management/patient_invoice.html", context)

@method_decorator(login_required, name='dispatch')
class PatientInvoiceView(ListView):
    model = CheckIn  
    template_name = 'patient_management/patient_invoice_final.html'
    success_url = reverse_lazy('patient_app:patientInvoice')
    form_class = Prescription_form

    def get(self, request, pk, *args, **kwargs):

        CheckIn_instance = CheckIn.objects.get(pk=pk)
        company = Company.objects.all().values()
        
        customer = Patient.objects.filter(pk=CheckIn_instance.patient.pk).values()
        customer_contact = ContactInformation.objects.filter(pk=CheckIn_instance.patient.pk).select_related('country').values()
        invoice = CheckIn.objects.filter(checkin_id=CheckIn_instance.checkin_id).prefetch_related('service', 'medication').first()
        services = invoice.service.all().values(
            'name',
            'category_id__name',
            'cost'
        )
        medication = Medicine_prescription.objects.filter(checkin_record_id=invoice).values(
            'prescribed_id__Inventory_code',
            'prescribed_id__desc',
            'prescribed_id__selling_price',
            'quantity',
            
            )
        
        vat_company = 0
        for comp in company:
            vat_per = comp['vat']
            vat_company = vat_per / 100
            
        
        total_med_cost = 0
        for item in medication:
            quantity = item['quantity']
            selling_price = item['prescribed_id__selling_price']
            cost_per_item = quantity * selling_price
            total_med_cost += cost_per_item
            item['cost'] = cost_per_item

        total_ser_cost = 0
        for ser in services:
            cost = ser['cost']
            total_ser_cost += cost  
        
        vat_par = Decimal(vat_company)
        sub_total = total_med_cost + total_ser_cost
        vat = sub_total * vat_par
        vat = vat.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        total_cost = sub_total + vat


        return render(request, self.template_name, {
            'totalInvoiceCost': total_cost,
            'vat': vat,
            'sub_total': sub_total,
            "checkId": CheckIn_instance,
            'services': services,
            'medication': medication,
            'cost_per_item': cost_per_item,
            'customer': customer,
            'customer_contact':customer_contact,
            'company': company
        })
       

