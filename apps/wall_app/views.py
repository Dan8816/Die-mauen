from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from apps.wall_app.models import User, UserManager, Message, Comment
from django.contrib import messages
import re, bcrypt

def index(request):
    return render(request, 'wall_temps/index.html')

def create(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
            print(errors)
            return redirect('/')
    else:
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['confirmpassword'].encode(), bcrypt.gensalt())
        )
        print("successfully created users")
        request.session['first_name']=request.POST['first_name']
        return redirect('/success')    

def login(request):
    if User.objects.filter(email=request.POST['email']):
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            print('email and password matches, successful login')
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['user_id'] = user.id
            return redirect('/success')
        else:
            print("failed password")

def success(request):
    context = {
        "messages" : Message.objects.all(),
        "users" : User.objects.all(),
        "comments" : Comment.objects.all()
    }
    return render(request, "wall_temps/success.html", context)

def logout(request):
    request.session.clear()    
    return redirect('/')

def create_msg(request):
    Message.objects.create(msg=request.POST["msg"], user_id=request.session['user_id'])
    return redirect('/success')

def create_cmnt(request):
    this_message = Message.objects.get(id=request.POST['id'])##later found this was not needed, below could have used msg_id = request.POST['id]
    Comment.objects.create(comnt=request.POST["cmnt"], msg_id=this_message.id,user_id=request.session['user_id'])
    return redirect('/success')
