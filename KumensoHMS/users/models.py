from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import os
from django.core.validators import RegexValidator
from django.db.models import Max
from django.dispatch import receiver
from django.db.models.signals import post_save
#from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, unique=False)
    def __str__(self):
        return self.name

class SysModel(models.Model):
    pass

class Country(models.Model):
    numeric_validator = RegexValidator(r'^[0-9]+$', 'Only numeric characters are allowed.')
    country_name = models.CharField(max_length=30)
    country_code = models.CharField(max_length=3 )
    country_no_code = models.CharField(
        max_length=3,
        validators=[numeric_validator],
        help_text='Enter phone number without country code'
    )
    def save(self, *args, **kwargs):
        # You can add phone number validation logic here if needed
        super().save(*args, **kwargs)

    def __str__(self):
        return self.country_name

class UserTitle(models.Model):
    title_code = models.CharField(max_length=5)
    title_name = models.CharField(max_length=50)

    def __str__(self):
        return self.title_code
    

class UserRoles(models.Model):
    role_code = models.CharField(max_length=50)
    role_name = models.CharField(max_length=50)
    role_desc = models.TextField(max_length=255, blank=True, null=True)
    role_status = models.CharField(max_length=255, choices=(('Active', 'Active'),('inactive', 'inactive')), default='Active')
                                                          

    def __str__(self):
        return self.role_code
    
class MaritalStatus(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=255, choices=(('Active', 'Active'),('inactive', 'inactive')), default='Active')

    def __str__(self):
        return self.name
    
class UserDesignation(models.Model):
    name = models.CharField(max_length=70, blank=True, null=True)
    status = models.CharField(max_length=255, choices=(('Active', 'Active'),('inactive', 'inactive')), default='Active')
    def __str__(self):
        return self.name
    
class Department(models.Model):
    name = models.CharField(max_length=70, blank=True, null=True)
    status = models.CharField(max_length=255, choices=(('Active', 'Active'),('inactive', 'inactive')), default='Active')
    def __str__(self):
        return self.name

class Gender(models.Model):
    name = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=255, choices=(('Active', 'Active'),('inactive', 'inactive')), default='Active')
    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    desc = models.CharField(max_length=255, null=True, blank=True)
    company_code = models.CharField(max_length=255, null=True, blank=True, editable=False)
    contact_no = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    town = models.CharField(max_length=255, null=True, blank=True)
    tpin = models.BigIntegerField(null=True, blank=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='companies', blank=True, null=True)
    vat = models.DecimalField(max_digits=5,decimal_places=2,null=True, blank=True)
    def save(self, *args, **kwargs):
        if self.name:
            # Get the first four characters of the input name
            first_four_chars = self.name[:4]
            # Concatenate with a number starting from 100
            max_existing_number = MyUser.objects.aggregate(Max('id'))['id__max']
            next_number = max_existing_number + 1 if max_existing_number else 100
            # Assign the concatenated result to company_code
            self.company_code = f"{first_four_chars}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company_code

class MyUser(AbstractUser):
    dateofbirth = models.DateField(verbose_name='Date of Birth', null=True, blank=True)
    title_code = models.ForeignKey('UserTitle', on_delete=models.CASCADE, related_name='users', blank=True, null=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='users', blank=True, null=True)
    designation = models.ForeignKey('UserDesignation', on_delete=models.CASCADE, related_name='users', blank=True, null=True)
    marital_status = models.ForeignKey('MaritalStatus', on_delete=models.CASCADE, related_name='users', blank=True, null=True)
    user_roles = models.ForeignKey('UserRoles', on_delete=models.CASCADE, related_name='users', blank=True, null=True)
    attention = models.ManyToManyField('Status', blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users', blank=True, null=True)
    first_name = models.CharField(max_length=30)  # Making first name mandatory
    last_name = models.CharField(max_length=150)  # Making last name mandatory
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, related_name='users', blank=True, null=True)
    address = models.TextField(max_length=250, null=True, blank=True,)
    phone_number_1 = models.CharField(max_length=250, blank=True, null=True)
    phone_number_2 = models.CharField(max_length=250, blank=True, null=True)
    biography = models.TextField(max_length=250, null=True, blank=True,)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='users', blank=True, null=True)
    def __str__(self):
        return self.username
    

class Profile(models.Model):

    def default_image_path(self):
        return os.path.join(os.path.dirname(__file__), 'path', 'to', 'default.webp')
   
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.webp', upload_to='images/profile/', null=True, blank=True)
    #image = models.ImageField(default=default_image_path, upload_to='images/profile/', null=True, blank=True)
    


    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        if self.image and self.image.size > 1000000:
            img = Image.open(self.image)
            output = BytesIO()
            img.save(output, format='JPEG', quality=70)
            output.seek(0)
            self.image = InMemoryUploadedFile(output,
                                              'ImageField',
                                              f"{self.image.name.split('.')[0]}.jpg",
                                              'image/jpeg',
                                              sys.getsizeof(self.image),
                                              None)
        super().save(*args, **kwargs)


class Revenue(models.Model):
    name = models.CharField(max_length=70, blank=True, null=True)
    code = models.CharField(max_length=10, unique=True, editable=False)
    status = models.CharField(max_length=255, choices=(('Active', 'Active'),('inactive', 'inactive')), default='Active')
    
    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.pk:  # Only generate code for new instances
            last_instance = Revenue.objects.order_by('-code').first()
            if last_instance:
                last_code = last_instance.code
                last_number = int(last_code[1:])  # Extract the number part of the code
                new_number = last_number + 1
                new_code = 'R' + str(new_number).zfill(4)  # Increment the number and format it
            else:
                new_code = 'R0001'  # If it's the first instance, start with R0001
            self.code = new_code
        super().save(*args, **kwargs)

class Inventory(models.Model):
    name = models.CharField(max_length=70, blank=True, null=True)
    code = models.CharField(max_length=10, unique=True, editable=False)
    status = models.CharField(max_length=255, choices=(('Active', 'Active'),('inactive', 'inactive')), default='Active')
    
    def __str__(self):
        return f"{self.code}-{self.name}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Only generate code for new instances
            last_instance = Inventory.objects.order_by('-code').first()
            if last_instance:
                last_code = last_instance.code
                last_number = int(last_code[1:])  # Extract the number part of the code
                new_number = last_number + 1
                new_code = 'I' + str(new_number).zfill(4)  # Increment the number and format it
            else:
                new_code = 'I0001'  # If it's the first instance, start with I0001
            self.code = new_code
        super().save(*args, **kwargs)

class Expenses(models.Model):
    name = models.CharField(max_length=70, blank=True, null=True)
    code = models.CharField(max_length=10, unique=True, editable=False)
    status = models.CharField(max_length=255, choices=(('Active', 'Active'),('inactive', 'inactive')), default='Active')
    
    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.pk:  # Only generate code for new instances
            last_instance = Expenses.objects.order_by('-code').first()
            if last_instance:
                last_code = last_instance.code
                last_number = int(last_code[1:])  # Extract the number part of the code
                new_number = last_number + 1
                new_code = 'M' + str(new_number).zfill(4)  # Increment the number and format it
            else:
                new_code = 'M0001'  # If it's the first instance, start with I0001
            self.code = new_code
        super().save(*args, **kwargs)

class GeneralExpenses(models.Model):
    name = models.CharField(max_length=70, blank=True, null=True)
    code = models.CharField(max_length=10, unique=True, editable=False)
    status = models.CharField(max_length=255, choices=(('Active', 'Active'),('inactive', 'inactive')), default='Active')
    
    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.pk:  # Only generate code for new instances
            last_instance = GeneralExpenses.objects.order_by('-code').first()
            if last_instance:
                last_code = last_instance.code
                last_number = int(last_code[1:])  # Extract the number part of the code
                new_number = last_number + 1
                new_code = 'G' + str(new_number).zfill(4)  # Increment the number and format it
            else:
                new_code = 'G0001'  # If it's the first instance, start with I0001
            self.code = new_code
        super().save(*args, **kwargs)

class inventory_List(models.Model):
    #name = models.CharField(max_length=70)
    desc = models.CharField(max_length=255)
    Inventory_code = models.ForeignKey(Inventory, on_delete=models.CASCADE,)
    quantity_in = models.IntegerField()
    total_cost = models.DecimalField(max_digits=6, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=6, decimal_places=2)
    quantity_out = models.IntegerField(blank=True, null=True)
    selling_price = models.DecimalField(max_digits=6, decimal_places=2)
    Quantity_Bal = models.IntegerField(blank=True, null=True)
    book_Bal = models.DecimalField(max_digits=6, decimal_places=2)
    barcode = models.BigIntegerField(blank=True, null=True)
    status = models.CharField(max_length=255, choices=(('Active', 'Active'),('inactive', 'inactive')), default='Active')

    def __str__(self):
        return self.desc


class Medicine_Category(models.Model):
    name = models.CharField(max_length=70, blank=True, null=True)
    #code = models.CharField(max_length=10, unique=True, editable=False)
    status = models.CharField(max_length=255, choices=(('Active', 'Active'),('inactive', 'inactive')), default='Active')
    
    def __str__(self):
        return self.name
class Medicine(models.Model):
    drug_name = models.CharField(max_length=70, blank=True, null=True)
    category = models.ForeignKey(Medicine_Category, on_delete=models.CASCADE,)
    quantity = models.IntegerField(blank=True, null=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2,blank=True, null=True)
    
    def __str__(self):
        return self.drug_name



class Services_Category(models.Model):
    name = models.CharField(max_length=70, blank=True, null=True)
    status = models.CharField(max_length=255, choices=(('Active', 'Active'),('inactive', 'inactive')), default='Active')
    def __str__(self):
        return self.name
class Services(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Services_Category, on_delete=models.CASCADE,)
    cost = models.DecimalField(max_digits=6, decimal_places=2,blank=True, null=True)
    disc_amount = models.DecimalField(max_digits=6, decimal_places=2,blank=True, null=True)
    def __str__(self):
        return self.name