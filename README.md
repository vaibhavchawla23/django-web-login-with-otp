# ASMIS Login Portal

ASMIS Web Portal for Appointment Reservation. The project covers basic functionality of secure login and logout by employing One Time Password.
The Project is coded using python3, Django 3.2 and Django Crispy Forms 1.11.2

## Dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install django and django-crispy-forms.

```bash
python3 -m pip install --upgrade pip
pip install django==3.2 django-crispy-forms==1.11.2
```
## Usage Instructions

```bash

codio@mercury-export:~/workspace$ python3 DJANGO/UNIT12/manage.py runserver 0.0.0.0:8000
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
April 17, 2021 - 20:19:14
Django version 3.2, using settings 'UNIT12.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
[17/Apr/2021 20:21:13] "GET / HTTP/1.1" 200 1747
User ID and Password OK For =  Alice
OTP Refreshed! 2B35Bb
Fresh OTP Successfully Published For =  Alice
[17/Apr/2021 20:21:26] "POST / HTTP/1.1" 302 0
User is Active
[17/Apr/2021 20:21:26] "GET /verify/ HTTP/1.1" 200 1549
CODE from DB 2B35Bb CODE entered by Alice 2B35Bb
OTP Validated , Proceeding for Login.
OTP Refreshed! 1cCEEc
User ID and Password OK For =  Alice
OTP Refreshed! c45d5A 
Fresh OTP Successfully Published For =  Alice   
[17/Apr/2021 20:21:58] "POST /verify/ HTTP/1.1" 302 0
Alice Appointment object (b5b2db00-6298-4f19-bc68-3bf85de94dc1)
[17/Apr/2021 20:21:59] "GET /profile/ HTTP/1.1" 200 1050

```
When using Codio the server is Available https://mercury-export-8000.codio-box.uk/   

# Structure
models.py
-
#### CustomUser
Models inherit AbstractUser from django.contrib.auth.models as CustomUser enabling us to use already available functions for Authentication like forms and password validation functions. 
The 
CustomUser is inherited again to make two variants of users differentiated by a flag is_doctor namely Patients & Doctors. Username and Passwords are same for ease usability and to show Case sensitivity.

- Patients {Already Created}
-- Alice
-- Bob
-- Carol
- Doctors {Already Created}
-- Dave 
-- Erin
-- Frank

```python
class CustomUser(AbstractUser):
  is_doctor = models.BooleanField(default=False, editable=False)

class Doctor(CustomUser):
  Dept = models.CharField(blank=False,max_length=100)

class Patient(CustomUser):
  Age = models.IntegerField(blank=False)
  Height = models.IntegerField(blank=False)
  Weight = models.IntegerField(blank=False)
```
#### Code [One Time Password]
Models also makes class Code that generate code whenever any user is logging in. This is triggered using signals. This can be integrated with third party extensions like twilio down the line.
As for the project the OTP is generated and displayed on the terminal hosting the manage.py .

```bash
OTP Refreshed! c45d5A # <<=== NEW OTP 
```
Salient features for the code here include:
-- Generate 6 Character Hex OTP to increase the complexity. 
['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F'].
-- OTP are case sensitive.
-- OTP is refreshed whenever used to avoid re-use of stale OTP.

```python
class Code(models.Model):
    number  = models.CharField(blank=True,max_length=6)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.number)
    
    def save(self, *args, **kwargs):
        hex_list = list(string.hexdigits)
        code_items=[]
        for i in range (6): 
            hex=random.choice(hex_list)
            code_items.append(hex) 
        code_string="".join(str(item) for item in code_items)
        print ("OTP Refreshed!", code_string)
        self.number=code_string
        super().save(*args, **kwargs)
```
views.py
-
Views is used make the backend flow between the flow.


#### verify_view
This 'verify_view' is used to verify the OTP and grant access only when the OTP is validated. 
```python
def verify_view(request, *args,**kwargs):
    form = CodeForm(request.POST or None)
    request.session['pk'] = request.user.pk
    pk = request.session.get('pk')
    if pk:
      user = CustomUser.objects.get(pk=pk)
      code = user.code
      if not request.POST and user.is_active:
        print ('User is Active')
        pass
      if form.is_valid():
          num=form.cleaned_data.get('number')
          print ('CODE from DB',code,'CODE entered by', user, num)
          if str(code) == num:
            print ('OTP Validated , Proceeding for Login.')
            code.save()
            login(request, user)
            return redirect(profile_view)
          else:
            return render (request, "auth.html", {'form': form} )
    return render (request, "verify.html", {'form': form} )
```

#### profile_view
This 'profile_view' shows different layouts based on user logged in. Its different for Patients and Doctors.

```python
def profile_view (request, *args,**kwargs):
    current_user = CustomUser.objects.get(username = request.user)
    if current_user.is_doctor:
      obj = Doctor.objects.get(username = request.user)
      aobj= Appointment.objects.get(doctor_id = request.user)
      temp = Patient.objects.get(username = aobj.patient_id)      
      print(obj,aobj)

    else :
      obj = Patient.objects.get(username = request.user)
      aobj= Appointment.objects.get(patient_id = request.user)
      temp = Doctor.objects.get(username = aobj.doctor_id)
      print(obj,aobj)
    context = {
        'object': obj ,
        'aobject': aobj,
        'Doctor' : temp
    }
    return render(request, "profile.html", context )
```
signals.py
-
Signals are used to trigger action based on events. In this case the they are used to generate a new OTP at every successful login attempt (using username and password). 

```python
@receiver (user_logged_in)
def update_profile(sender, user, request, **kwargs):
    if user_logged_in:
      print ("User ID and Password OK For = " ,user)
      if Code.objects.update_or_create(user=user):
        print ("Fresh OTP Successfully Published For = " ,user)

```
# Tests
The system is tests on various real-life flows for the following scenarios:
- Username Password and OTP are Case Sensitive.
- Protection against Stale OTP.
- Independent Profile Pages for Patient and Doctor using the same login page.
-- Patient can see Appointment details like Doctor Name and Department.
-- Doctor can see upcoming Patient Name.
- No DJANGO Admin Login; This ensures that No user has Admin access database as admin.
- Passwords in the Database are stored in encrypted format
- The system also logs confirmation of OTP generation and their requesting usernames. 
```bash
codio@mercury-export:~/workspace/DJANGO/UNIT12$ sqlite3
SQLite version 3.23.1 2018-04-10 17:39:29
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite> .open db.sqlite3
sqlite> .tables
ASMIS_appointment                  auth_group                       
ASMIS_code                         auth_group_permissions           
ASMIS_customuser                   auth_permission                  
ASMIS_customuser_groups            django_admin_log                 
ASMIS_customuser_user_permissions  django_content_type              
ASMIS_doctor                       django_migrations                
ASMIS_patient                      django_session
sqlite> .mode column
sqlite> select * from ASMIS_customuser;
1           pbkdf2_sha256$260000$VmivUzBY4WTR4HO8oOhFpD$ZCHKlBG1tGeOggpKy9F/vIzUsT/hwm+WjtD44K0l6JU=  2021-04-17 21:41:00.640889  0             Alice                                           0           1           2021-04-17 20:37:02.831335  0         
2           pbkdf2_sha256$260000$BKDIqeMJGqPzdpIvu4wXta$d/CiiebBw24Vhnus5x5Ni+ePZPufZqF138wZYE+mrBk=  2021-04-17 21:15:37.036470  0             Bob                                             0           1           2021-04-17 20:37:03.223808  0         
3           pbkdf2_sha256$260000$zIiH3A2nnzISRSwM6JbbMs$6ABZrbHiND/b7jYEOjrbAeHu0n3p8BKSca8+jWwEXsY=  2021-04-17 20:37:58.056334  0             Carol                                           0           1           2021-04-17 20:37:03.831959  0         
4           pbkdf2_sha256$260000$8BJbHWVikaXVQgpt0KnVfD$LXQLLnfBbfzF+wV53xeiRgMSail/8zNBTLOHpjFBoxs=                              0             Dave                                            0           1           2021-04-17 20:37:04.239087  1         
5           pbkdf2_sha256$260000$9P4l9Mbw1EuRzdA6Ig1dSS$VcuvRI62TuI93wRWAL7+hHDpaJEvXa3hKRWrQ5FcPcQ=                              0             Erin                                            0           1           2021-04-17 20:37:04.556792  1         
6           pbkdf2_sha256$260000$EFHz3qyg6OvhE43o0Zb9cG$bC64GJQ2ftoPyjI9ruC6Ly6C/oyNApybfc2JdWUb070=                              0             Frank                                           0           1           2021-04-17 20:37:05.034603  1    
```
## If Database is to be re populated
```bash
# Delete database : 
rm -f /home/codio/workspace/DJANGO/UNIT12/db.sqlite3

# Use Django Shell to re-create the users and appointments 
python3 /home/codio/workspace/DJANGO/UNIT12/manage.py shell

```
```python
from ASMIS.models import Patient ,Appointment, Doctor 
Alice = Patient.objects.create_user(username='Alice', password='Alice', Age='43', Height='160', Weight='60')
Alice.save()
Bob = Patient.objects.create_user(username='Bob', password='Bob', Age='33', Height='180', Weight='80')
Bob.save()
Carol= Patient.objects.create_user(username='Carol', password='Carol', Age='23', Height='150', Weight='50')
Carol.save()
Dave = Doctor.objects.create_user(username='Dave', password='Dave',is_doctor='True', Dept='Gastronomy')
Dave.save()
Erin = Doctor.objects.create_user(username='Erin', password='Erin',is_doctor='True', Dept='Orthopedics')
Erin.save()
Frank = Doctor.objects.create_user(username='Frank', password='Frank',is_doctor='True', Dept='General Physician')
Frank.save()


A=Patient.objects.get(username='Alice')  
X=Doctor.objects.get(username='Dave')  
App = Appointment.objects.create( patient_id=A, doctor_id=X)  

B=Patient.objects.get(username='Bob')  
Y=Doctor.objects.get(username='Erin')  
App = Appointment.objects.create( patient_id=B, doctor_id=Y)

C=Patient.objects.get(username='Carol')  
Z=Doctor.objects.get(username='Frank')  
App = Appointment.objects.create( patient_id=C, doctor_id=Z)

Appointment.objects.all()

```
# References 
#### _Simple two factor authentication in Django with SMS verification code | basic 2fa using Twilio_
[https://www.youtube.com/watch?v=YA4ZPKTPicw] 
#### _2fa explained: How to enable it and how it works_
[https://www.csoonline.com/article/3239144/2fa-explained-how-to-enable-it-and-how-it-works.html]
#### _Python Django Web Framework - Full Course for Beginners_
[https://www.youtube.com/watch?v=F5mRW0jo-U4]