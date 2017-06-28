from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Poke

# Create your views here.
def index(request):
    return render(request, 'loginReg_app/index.html') 

def register(request):
    if request.method == "POST":
        response = User.objects.validateUser(request.POST)
        if response['status']:  # True
            user = response['user']  # Newly created user
            request.session['user_id'] = user.id
            return redirect('/pokes')
        else:
            for error in response['errors']:
                messages.add_message(request, messages.ERROR, '{}'.format(error))
            return redirect('/')

def login(request):
    loginChk, login_response, errors = User.objects.login(request.POST)

    if loginChk:  # True -> login email and corresponding pwd found
        request.session['user_id'] = login_response.id
        return redirect("/pokes")
    else:
        for error in errors:
            messages.add_message(request, messages.ERROR, '{}'.format(error))
        # messages.info(request, errors)
        return redirect('/')

# def postPoke(request):
#     if request.method == "GET" and "user_id" in request.session:
#         Poke.objects.pokeCount(request.session['user_id'])

def newPoke(request, id):
    # id = Person you are trying to poke
    # when button is clicked poke count should increment
    # try:
    #     Poke.objects.countPoke(id=id)

    if not 'count' in request.session:
        request.session['count'] = 0
    
    result = Poke.objects.checkPoke(request.session['count'], id)

    if result[0]:
        request.session['count'] += 1
        messages.info(request, result[1])
    else:
        messages.error(request, result[1])

    return redirect('/pokes')

def pokes(request):
    user = User.objects.get(id=request.session['user_id'])
    messages.add_message(request, messages.SUCCESS, "Welcome, %s!" % (user.name))

    context = {
        "count":request.session['count'],
        "users":User.objects.all()
    }

    return render(request, 'loginReg_app/pokes.html', context) 