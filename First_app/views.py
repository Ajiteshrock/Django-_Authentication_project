#ZCRMRestClient.initialize(configuration
from django.shortcuts import render ,redirect
from django.http import HttpResponse
from .forms import UserForm,UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
import zcrmsdk
import requests

api = requests.get('https://www.zohoapis.com/crm/v2/settings/modules')


# Create your views here.
def index(request):
    dic = {'me':100}
    return render(request,'index.html',dic)

@login_required   
def user_logout(request):
    logout(request)
    return redirect('/')

def registered(request):
    registered = False

    if request.method == 'POST':

        user_from = UserForm(data = request.POST)
        profile_form = UserProfileInfoForm(data = request.POST)

        if user_from.is_valid() and  profile_form.is_valid():

            user = user_from.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            #profile.set_password(profile.password)
            profile.user = user #onetoone relation
            
            
            if 'profile_pic' in request.FILES:
                print("found")
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_from.errors , profile_form.errors)
    else:
        user_from = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'reg.html',{'user_form':user_from,
                                      'profile_form':profile_form  ,
                                      'registered':registered})

def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'login.html', {})
