from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from core.models import Profile, Website
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
# from twilio.rest import Client
import json
import os
import requests
import smtplib



# Create your views here.
@login_required(login_url='signin')
def getstats(request):
    # Retrieve the logs from the database
    logs = Website.objects.all()

    # Convert the logs to a JSON object
    data = []
    for log in logs:
        data.append({
            "user_id": log.user_id,
            'user': log.user.username,
            "timestamp": log.timestamp,
            "is_url_valid": log.is_url_valid,
            "websites": log.websites,
            "is_active": log.is_active
        })
    data = json.dumps(data, indent=1, sort_keys=True, cls=DjangoJSONEncoder)

    # Return the data as a JSON response
    return (data)           #JsonResponse(data, safe=False)

def is_string_an_url(url_string: str):
    validate_url = URLValidator()

    try:
        validate_url(url_string)
        return True

    except Exception:
        return False


def get_response(url):
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        return ('website down')
    return ('website up')


def send_notification(message, recipients):
    # Replace "sender@example.com" and "password" with the appropriate values
    sender = 'akanbi.ges201@gmail.com' #os.environ.get('EMAIL_ADD')
    password = 'paifygabkkfhxwmf' #os.environ.get('APP_PASSWORD')
        
    # Connect to the SMTP server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender, password)
        
    # Send the email
    server.sendmail(sender, recipients, message)
        
    # Disconnect from the SMTP server
    server.quit()



@login_required(login_url='signin')
def index(request):
    subject = "Website monitoring update"
    body = 'The website is currently DOWN'
    message = f"Subject: {subject}\n\n{body}"
    recipients = ["a_olartunde@yahoo.com", "olarrtt@icloud.com"]
    if request.method == 'POST':
        valid_urls = []
        data = request.POST.get("web_list").split(", ")
        for url in data:
            if is_string_an_url(url) is True:
                valid_urls.append(url)
                print (valid_urls)
                websites_lists = Website.objects.create(websites=url, user=request.user, timestamp = timezone.now(), is_url_valid = f'{url} is valid', is_active = get_response(url))
            else:
                websites_lists = Website.objects.create(websites=url, user=request.user, timestamp = timezone.now(), is_url_valid = f'{url} is not valid', is_active = 'website down')
     
        for v_url in valid_urls:
           if get_response(v_url) is False:
                send_notification(message, recipients)
                
        websites_lists.save()
        web_list = Website.objects.filter(user=request.user)
        return render(request, 'index.html', {'web_list': web_list})
        
    elif request.method  == 'GET':
        return render(request, 'index.html')

def signup(request, method=['GET', 'POST']):
    """returns the render of the signup page for users

    Args:
        request (any): django request module
    """
    if request.method =='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm password']
        
        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect(request, 'signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username already exists')
                return redirect(request, 'signup')
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            user_login = auth.authenticate(username=username, password=password)
            auth.login(request, user_login)

            #create a Profile object for the new user
            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
            new_profile.save()
            return redirect('index')
        
        messages.info(request, 'Password Not Matching') 
        return redirect('signup')
    return render(request, 'signup.html')


def signin(request, method=['GET', 'POST']):
    """ """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)

        if user != None:
            auth.login(request, user)
            return redirect(index)
        messages.info(request, 'Wrong Username or Password')
        return redirect('signin')
        
    return render(request, 'signin.html')


@login_required(login_url='signin')
def logout(request, method=['GET', 'POST']):
    auth.logout(request)
    return redirect('signin')