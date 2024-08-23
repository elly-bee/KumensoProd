from django.urls import path
from . import views as users
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'user_app'

urlpatterns = [
    path('', users.home, name='home'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('users/userlist', users.UserCreateView.as_view(), name='userlist'),
    path('users/', users.UserListView.as_view(), name='list'),
    path('dashboard/', users.HomeListView.as_view(), name='dashboard'),
    path('users/add', users.UserCreateView.as_view( template_name = 'users/add-user.html'), name='adduser'),
    path('users/delete/<int:pk>', users.UserDeleteView.as_view(template_name = 'base/modelForms.html'), name='delete'),
    path('users/edit/<int:pk>', users.UserUpdateView.as_view(), name='useredit'),
    path('users/passwordreset/<int:pk>', users.UserPasswordRestView.as_view(), name='passwordreset'),   
    path('users/profile/<int:pk>', users.UserProfile.as_view(), name='profile'), 
    path('users/role/', users.UserListView.as_view(template_name='users/userroleupdate.html'), name='userrole'), 
    #path('country/edit/<int:pk>', users.CountryUpdateView.as_view(), name='countryedit'),   
    path('company/country/', users.CountryListView.as_view(), name='countrymng'),
    path('company/Depatment/', users.DeptListView.as_view(), name='Deptlist'),
    path('company/Revenue/', users.RevenueListView.as_view(), name='Revenuelist'),
    path('company/Servicelist/', users.ServiceListView.as_view(), name='Servicelist'),
    path('company/Inventory/', users.InventoryListView.as_view(), name='Inventorylist'),
    path('company/Inventorylist_List/', users.inventoryList_ListView.as_view(), name='Inventorylist_List'),
    path('company/Expenseslist/', users.ExpensesListView.as_view(), name='Expenseslist'),
    path('company/generalExpenseslist/', users.GeneralExpensesListView.as_view(), name='generalExpenseslist'),
    path('company/Designation/', users.DesignationListView.as_view(), name='Desgnlist'),
    path('company/Gender/', users.MaritalStatusView.as_view(), name='maritallist'),
    path('company/UserRoles/', users.UserRolesView.as_view(), name='userroleslist'),
    path('company/UserRoles/<int:pk>', users.UserRolesView.as_view(), name='userrolesdelete'),
    
    #path('company/<int:pk>', users.CompanyView.as_view(), name='company'),  

    # Define other URL patterns as needed
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)