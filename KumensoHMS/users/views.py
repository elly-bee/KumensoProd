
import sys
import os
parent_dir = os.path.abspath("..")

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,TemplateView,FormView
from django.contrib.auth.views import PasswordResetView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from patient_management.models import *




"""class MyMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_type == 'admin'"""


@login_required()
def home(request):
    """ Home Page """
    return redirect(reverse_lazy('user_app:dashboard'))

@method_decorator(login_required, name='dispatch')
class UserCreateView(CreateView):
    """ Create a new User by Admin """
    model = MyUser
    form_class = UserCreateForm
    #template_name = 'users/add-user.html'
    success_url = reverse_lazy('user_app:list')
    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        messages.success(self.request, f"{user.username} is created successfully!")
        user.save()
        return redirect(reverse_lazy('user_app:list'))
    
@method_decorator(login_required, name='dispatch')  
class UserListView(ListView):
    """ List of Users for Admin """
    model = MyUser
    template_name = 'users/userlist.html'
    context_object_name = 'data'

@method_decorator(login_required, name='dispatch')
class HomeListView(ListView):
    model = Country
    template_name = 'users/index.html'
    success_url = reverse_lazy('user_app:dashboard')
    form_class = CountryaddForm  # Default blank form class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Combine queryset data from multiple models
        userId = self.request.user.id
        context['Country_form'] = CountryaddForm()
        company = Company.objects.all()
        current_date = datetime.now().date()
        appointments = Appointments.objects.filter(Q(doctor=userId) & Q(appointment_date__gte=current_date))
        Upappointments = Appointments.objects.filter(Q(appointment_date__gte=current_date))
        print(appointments)
        
        context['countrydata'] = {
            'countries': Country.objects.all(),
            'userTitles': UserTitle.objects.all(),
            'userRoles': UserRoles.objects.all(),
            'maritalStatuses': MaritalStatus.objects.all(),
            'userDesignations': UserDesignation.objects.all(),
            'departments': Department.objects.all(),
            'genders': Gender.objects.all(),
            'companies': company,
            'doctor': MyUser.objects.filter(designation__name='Doctor'),
            'users': MyUser.objects.all(),
            'appointments': appointments.count(),
            'upappointments': Upappointments.count(),
            'appointmentList': Upappointments.values()
        }
        return context
    
""" item management for system parameters"""
@method_decorator(login_required, name='dispatch')
class CountryListView(CreateView):
    model = Country
    template_name = 'users/countrylist.html'
    success_url = reverse_lazy('user_app:countrymng')
    form_class = CountryaddForm  # Default blank form class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Country_form'] = CountryaddForm()
        context['countrydata'] = {
            'countries': Country.objects.all(),
        }
        return context
@method_decorator(login_required, name='dispatch')    
class DeptListView(CreateView):
    model = Department
    template_name = 'users/Deptlist.html'
    success_url = reverse_lazy('user_app:Deptlist')
    form_class = DeptCreateForm  # Default blank form class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Combine queryset data from multiple models
        context['Dept_form'] = DeptCreateForm()
        context['Dept_data'] = {
            'departments': Department.objects.all(),
        }
        return context
@method_decorator(login_required, name='dispatch')   
class DesignationListView(CreateView):
    model = UserDesignation
    template_name = 'users/Designlist.html'
    success_url = reverse_lazy('user_app:Desgnlist')
    form_class = UserDesignationForm  # Default blank form class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Combine queryset data from multiple models
        context['Design_form'] = UserDesignationForm()
        context['Design_data'] = {
            'userDesignations': UserDesignation.objects.all(),
        }
        return context

@method_decorator(login_required, name='dispatch')
class MaritalStatusView(CreateView):
    model = MaritalStatus
    template_name = 'users/maritallist.html'
    success_url = reverse_lazy('user_app:maritallist')
    form_class = MaritalStatusForm  # Default blank form class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Combine queryset data from multiple models
        context['MaritalStatus_form'] = MaritalStatusForm()
        context['MaritalStatus_data'] = {
            'MaritalStatus': MaritalStatus.objects.all(),
        }
        return context
@method_decorator(login_required, name='dispatch')
class UserRolesView(CreateView):
    model = UserRoles
    template_name = 'users/userroles.html'
    success_url = reverse_lazy('user_app:userroleslist')
    form_class = UserRolesForm  # Default blank form class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Combine queryset data from multiple models
        context['UserRoles_form'] = UserRolesForm()
        context['UserRoles_data'] = {
            'userRoles': UserRoles.objects.all(),
        }
        return context
    
""" item management for system parameters"""



@method_decorator(login_required, name='dispatch')
class UserDeleteView( DeleteView):
    """ Delete a user by Admin """
    model = MyUser
    
    success_url = reverse_lazy('user_app:list')

    def form_valid(self, form):
        super(UserDeleteView, self).form_valid(form)
        messages.warning(self.request, f"user is deleted successfully!")
        return redirect(reverse_lazy('user_app:list'))
@method_decorator(login_required, name='dispatch')    
class UserUpdateView(UpdateView):
    """ Update a user by Admin """
    model = MyUser
    form_class = UserUpdateForm
    template_name = 'users/edituser.html'
    success_url = reverse_lazy('user_app:list')


    def form_valid(self, form):
        super(UserUpdateView, self).form_valid(form)
        messages.success(self.request, f"user is updated successfully!")
        return redirect(reverse_lazy('user_app:list'))
    


    

"""class CreateCountryView(CreateView):
    model = Country
    form_class = CountryaddForm
    success_url = reverse_lazy('user_app:param')"""
@method_decorator(login_required, name='dispatch')
class UserRoleView(UpdateView):
    model = MyUser
    form_class = UserUpdateForm
    #template_name = 'users/edituser.html'
    success_url = reverse_lazy('user_app:list')


    def form_valid(self, form):
        super(UserUpdateView, self).form_valid(form)
        messages.success(self.request, f"user is updated successfully!")
        return redirect(reverse_lazy('user_app:list'))
@method_decorator(login_required, name='dispatch')
class CompanyView(ListView):
    model = Company
    form_class = CompanyForm
    template_name = 'users/companysettings.html'
    success_url = reverse_lazy('user_app:list')


    def form_valid(self, form):
        super(CompanyView, self).form_valid(form)
        messages.success(self.request, f"user is updated successfully!")
        return redirect(reverse_lazy('user_app:list'))

@method_decorator(login_required, name='dispatch')
class UserProfile(UpdateView):

    def get(self, request, **kwargs):
        user = request.user
        data = MyUser.objects.get(id=user.id)
        print(data, user)
       
        c_form = UserUpdateForm(instance=user)
        p_form = CustomerProfileForm(instance=user.profile)
        

        context = {
            'data': data,
            'c_form': c_form,
            'p_form': p_form,
        }
        return render(request, 'users/edituser.html', context)

    def post(self, request, *args, **kwargs):
        user = request.user
        c_form = UserUpdateForm(request.POST, instance=user)
        p_form = CustomerProfileForm(request.POST, request.FILES, instance=user.profile)
        if c_form.is_valid() and p_form.is_valid():
            username = c_form.cleaned_data['username']
            c_form.save()
            p_form.save()
            messages.success(request, f"{username}'s profile has been updated successfully!")
        return redirect(reverse_lazy('user_app:profile', kwargs={'pk': user.id}))
@method_decorator(login_required, name='dispatch')
class UserPasswordRestView(PasswordResetView):
    """ Update a user by Admin """
    model = MyUser
    form_class = SetPasswordForm  # Change form_class to SetPasswordForm
    template_name = 'users/passwordrest.html'
    success_url = reverse_lazy('user_app:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.get_object()  # Get the user object
        kwargs['user'] = user  # Pass the user object to the form
        return kwargs

    def get_object(self):
        # Implement this method to retrieve the user object.
        # This depends on how your view is structured and how you identify the user.
        # For example:
        user_id = self.kwargs.get('pk')  # Assuming the user id is passed in the URL kwargs
        return get_object_or_404(MyUser, pk=user_id)

    def form_valid(self, form):
        form.save()  # Save the form (this will change the password)
        messages.success(self.request, "Password updated successfully!")
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class RevenueListView(CreateView):
    model = Revenue
    template_name = 'users/Revenuelist.html'
    success_url = reverse_lazy('user_app:Revenuelist')
    form_class = RevenueForm  # Default blank form class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Combine queryset data from multiple models
        context['Revenue_form'] = RevenueForm()
        context['Revenue_data'] = {
            'Revenues': Revenue.objects.all(),
        }
        return context
@method_decorator(login_required, name='dispatch')    
class InventoryListView(CreateView):
    model = Inventory
    template_name = 'users/Inventorylist.html'
    success_url = reverse_lazy('user_app:Inventorylist')
    form_class = InventoryForm  # Default blank form class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Combine queryset data from multiple models
        context['Inventory_form'] = InventoryForm()
        context['Inventory_data'] = {
            'Inventorys': Inventory.objects.all(),
        }
        
        return context
@method_decorator(login_required, name='dispatch')    
class ExpensesListView(CreateView):
    model = Expenses
    template_name = 'users/expenseslist.html'
    success_url = reverse_lazy('user_app:Expenseslist')
    form_class = ExpensesForm  # Default blank form class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Combine queryset data from multiple models
        context['Expenses_form'] = ExpensesForm()
        context['Expenses_data'] = {
            'Expensess': Expenses.objects.all(),
        }
        
        return context
@method_decorator(login_required, name='dispatch')    
class GeneralExpensesListView(CreateView):
    model = GeneralExpenses
    template_name = 'users/generalExpenseslist.html'
    success_url = reverse_lazy('user_app:generalExpenseslist')
    form_class = GeneralExpensesForm  # Default blank form class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Combine queryset data from multiple models
        context['gExpenses_form'] = GeneralExpensesForm()
        context['gExpenses_data'] = {
            'gExpensess': GeneralExpenses.objects.all(),
        }
        
        return context
@method_decorator(login_required, name='dispatch')    
class inventoryList_ListView(CreateView):
    model = inventory_List
    template_name = 'users/Inventorylist_List.html'
    success_url = reverse_lazy('user_app:Inventorylist_List')
    form_class = InventoryListForm  # Default blank form class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Combine queryset data from multiple models
        context['inventoryList_form'] = InventoryListForm()
        context['inventoryList_data'] = {
            'inventoryLists': inventory_List.objects.all(),
        }
        
        return context
@method_decorator(login_required, name='dispatch')
class ServiceListView(CreateView):
    model = Services
    template_name = 'users/servicelist.html'
    success_url = reverse_lazy('user_app:Servicelist')
    form_class = ServicesForm  # Default blank form class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Combine queryset data from multiple models
        context['service_form'] = ServicesForm()
        context['service_data'] = {
            'serviceLists': Services.objects.all(),
        }
        
        return context
