from django.http import HttpResponse
from django.shortcuts import render, redirect 
from .models import Patient , Doctor , Appointment , CustomUser
from .forms import CodeForm #, SymptomAppointmentForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
import pdb

# Create your views here.

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

def profile_view (request, *args,**kwargs):
    current_user = CustomUser.objects.get(username = request.user)
    if current_user.is_doctor:
      obj = Doctor.objects.get(username = request.user)
      aobj= Appointment.objects.get(doctor_id = request.user)
      temp = Patient.objects.get(username = aobj.patient_id)      

    else :
      obj = Patient.objects.get(username = request.user)
      aobj= Appointment.objects.get(patient_id = request.user)
      temp = Doctor.objects.get(username = aobj.doctor_id)
    context = {
        'object': obj ,
        'aobject': aobj,
        'Doctor' : temp
    }
    return render(request, "profile.html", context )