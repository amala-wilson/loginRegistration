from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    return render(request, 'loginReg_app/index.html') 

def register(request):
    if request.method == "POST":
        response = User.objects.validateUser(request.POST)
        if response['status']:  # True
            user = response['user']  # Newly created user
            request.session['user_id'] = user.id
            return redirect('/success')
        else:
            for error in response['errors']:
                messages.add_message(request, messages.ERROR, '{}'.format(error))
            return redirect('/')

def login(request):
    loginChk, login_response, errors = User.objects.login(request.POST)

    if loginChk:  # True -> login email and corresponding pwd found
        # request.session['first_name'] = login_response.first_name
        request.session['user_id'] = login_response.id
        return redirect("/success")
    else:
        for error in errors:
            messages.add_message(request, messages.ERROR, '{}'.format(error))
        # messages.info(request, errors)
        return redirect('/')

def success(request):
    user = User.objects.get(id=request.session['user_id'])
    messages.add_message(request, messages.SUCCESS, "Success! Welcome, %s!" % (user.first_name))
    messages.add_message(request, messages.SUCCESS, "Successfully registered (or logged in)!")
    return render(request, 'loginReg_app/success.html') 