
from django import forms
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from .models import *
from phonenumber_field.formfields import PhoneNumberField



class UserCreateForm(forms.ModelForm):
    """ User Create or Registration Form """
    #phone_number_1 = PhoneNumberField()
    #phone_number_2 = PhoneNumberField()
    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'department','title_code','designation','marital_status','user_roles','company','dateofbirth','gender','address','biography')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'type': 'email', 'class': 'form-control'}),
            'password': forms.TextInput(attrs={'type': 'password', 'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'title_code': forms.Select(attrs={'class': 'form-control'}),
            'designation': forms.Select(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'user_roles': forms.Select(attrs={'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'dateofbirth': forms.DateInput(attrs={'type': 'date','class': 'form-control'}), 
            'address' : forms.Textarea(attrs={'class': 'form-control','rows':'2'}),
            'biography' : forms.Textarea(attrs={'class': 'form-control','rows':'2'}),
            
                }
        def __init__(self, *args, **kwargs):
                            super().__init__(*args, **kwargs)
                            self.fields['dateofbirth'].required = True


class UserUpdateForm(forms.ModelForm):
    """ User Update Form by Admin """
    
    phone_number_2 = PhoneNumberField()
    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'username', 'email', 'department','title_code','designation','marital_status','user_roles','company','dateofbirth','country','address','biography','phone_number_1','phone_number_2','gender')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'type': 'email', 'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'title_code': forms.Select(attrs={'class': 'form-control'}),
            'designation': forms.Select(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'user_roles': forms.Select(attrs={'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'address' : forms.Textarea(attrs={'class': 'form-control','rows':'2'}),
            'biography' : forms.Textarea(attrs={'class': 'form-control','rows':'2'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),

        }


class CountryaddForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ('__all__' )
        widgets = {
            'country_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'country_code' : forms.TextInput(attrs={'class': 'form-control'}),
            'country_no_code' : forms.TextInput(attrs={'class': 'form-control'}),
        }
   


class DeptCreateForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name','status')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status' : forms.Select(attrs={'class': 'form-control'}),
            
                }
      
class UserDesignationForm(forms.ModelForm):
    class Meta:
        model = UserDesignation
        fields = ('name','status')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status' : forms.Select(attrs={'class': 'form-control'}),
            
                }
      

class MaritalStatusForm(forms.ModelForm):
    class Meta:
        model = MaritalStatus
        fields = ('name','status')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status' : forms.Select(attrs={'class': 'form-control'}),
            
                }


class UserRolesForm(forms.ModelForm):
    class Meta:
        model = UserRoles
        fields = ('__all__')
        widgets = {
            'role_code': forms.TextInput(attrs={'class': 'form-control'}),
            'role_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role_desc': forms.Textarea(attrs={'class': 'form-control'}),
            'role_status' : forms.Select(attrs={'class': 'form-control'}),
            
                }



class DefaltForm(forms.ModelForm):
    class Meta:
        model = SysModel
        fields =('__all__')
    pass



class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
        widgets = {
            'image': forms.FileInput(attrs={'type': 'file', 'class': 'form-control'}),
        }


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('__all__')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_code': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'contact_no' : forms.TextInput(attrs={'class': 'form-control'}),
            'tpin' : forms.TextInput(attrs={'class': 'form-control'}),
            'country' : forms.TextInput(attrs={'class': 'form-control'}),
            
                }



class SetPasswordForm(DjangoPasswordChangeForm):
    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
        help_text=("Enter a new password. Passwords must be at least 8 characters long and cannot be entirely numeric."),
    )
    new_password2 = forms.CharField(
        label=("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=("Enter the same password as before, for verification."),
    )

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password1
    


class RevenueForm(forms.ModelForm):
    class Meta:
        model = Revenue
        fields = ('name','status')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status' : forms.Select(attrs={'class': 'form-control'}),
            
                }
        
class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('name','status')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status' : forms.Select(attrs={'class': 'form-control'}),
            
                }


class InventoryListForm(forms.ModelForm):
    class Meta:
        model = inventory_List
        fields = ('desc', 'Inventory_code', 'quantity_in', 'total_cost', 'unit_cost', 'quantity_out', 'selling_price', 'Quantity_Bal', 'book_Bal', 'barcode', 'status')
        widgets = {
            'desc': forms.TextInput(attrs={'class': 'form-control'}),
            'Inventory_code': forms.Select(attrs={'class': 'form-control'}),
            'quantity_in': forms.TextInput(attrs={'class': 'form-control'}),
            'total_cost': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_cost': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity_out': forms.TextInput(attrs={'class': 'form-control'}),
            'selling_price': forms.TextInput(attrs={'class': 'form-control'}),
            'Quantity_Bal': forms.TextInput(attrs={'class': 'form-control'}),
            'book_Bal': forms.TextInput(attrs={'class': 'form-control'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ('name','status')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status' : forms.Select(attrs={'class': 'form-control'}),
            
                }
        
class GeneralExpensesForm(forms.ModelForm):
    class Meta:
        model = GeneralExpenses
        fields = ('name','status')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status' : forms.Select(attrs={'class': 'form-control'}),
            
                }
        
class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ('name','category','cost')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'cost' : forms.TextInput(attrs={'class': 'form-control'}),
            'disc_amount' : forms.TextInput(attrs={'class': 'form-control'}),
            }

