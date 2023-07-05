from .models import Project, Roadmap
from django.shortcuts import render,redirect, HttpResponse
from django.http import JsonResponse
import os
import openai
from dotenv import load_dotenv, find_dotenv
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.models import User
from growthing import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token

# Create your views here.
def project_list(request):
    projects = Project.objects.all()
    programming = Project.objects.filter(genre='programming')
    design = Project.objects.filter(genre='design')
    marketing = Project.objects.filter(genre='marketing')
    video_editing = Project.objects.filter(genre='video editing')
    misc = Project.objects.filter(genre='misc')
    return render(request, "explore.html", context={'projects':projects, 'programming':programming, 'design':design,'marketing':marketing,'video_editing':video_editing, 'misc':misc})

def home(request):
    return render(request, "ongoing.html")

def ongoing_project_list(request):
    projects = Roadmap.objects.all()
    programming = Roadmap.objects.filter(genre='programming')
    design = Roadmap.objects.filter(genre='design')
    marketing = Roadmap.objects.filter(genre='marketing')
    video_editing = Roadmap.objects.filter(genre='video editing')
    misc = Roadmap.objects.filter(genre='misc')
    return render(request, "myhome.html", context={'projects':projects, 'programming':programming, 'design':design,'marketing':marketing,'video_editing':video_editing, 'misc':misc})

def explore(request):
    context={
        
    }
    return render(request, "explore.html", context)

def assistant(request):
    context={
    "previos_chatings1":"this is your previous chattings"
    }
    return render(request,'assistant.html', context)

def ongoing(request): 
    context={
        "My_projects":"all my projects will be shown here"
    }
    return render(request,'ongoing.html', context)

def index(request):
    context={
        "index_content":'index ka content'
    }
    messages.success(request, 'this is test message')
    return render(request, 'index.html', context)

def project_content(request,pk):
    project = Project.objects.get(project_id = pk)
    return render(request,'project.html', context={'project':project })

def show_roadmap(request):
    roadmap_url = f'/roadmap/{pk}'
    return redirect('roadmap_url')

roadmap_status = {}

def generate_roadmap(request,pk):
    global roadmap_status
    
    if pk in roadmap_status and roadmap_status[pk]:
        roadmap_content = Roadmap.objects.get(project_id = pk)
        lines = roadmap_content.generate_roadmap.split('\n')
        return render(request, 'roadmap.html', {'roadmap':roadmap_content, 'lines': lines})

    else:

        api_key = settings.OPENAI_SETTINGS['api_key']

    openai.api_key = api_key
    # Retrieve projects from the database
    project = Project.objects.get(project_id = pk)

    # Make request to OpenAI API
    response = openai.Completion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #             {"role": "system", "content": "You are a helpful assistant."},
    #             {"role": "user", "content": "Who won the world series in 2020?"},
    #             {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    #             {"role": "user", "content": "Where was it played?"}
    # ]

         engine="text-davinci-003",
         prompt=f"I want to make a project in {project.genre} which is I want to {project.title}.{project.description}. You have to make a roadmap for the project such a way that I can learn the required skills and then implement them. Keep the work as minimised as possible and be objective orientated. Properly define each step and tasks to be done in each step. Make sure your output has each step separated by /n and in each step, tasks should be separated useing ','. ",
         max_tokens=500,
         temperature=1,  
         n=1,  
         stop=None,
    )
    
    # Process the API response
    generated_roadmap = response.choices[0].text.strip()
    # Save the roadmap in the 'roadmap' database
    roadmap = Roadmap(
        generate_roadmap=generated_roadmap,
        title = project.title,
        description = project.description,
        skills = project.skills,
        genre = project.genre,
        project_id = project.project_id,
    )
    roadmap.save()

    roadmap_status[pk] = True
    lines = roadmap.generate_roadmap.split('\n')

    return render(request, 'roadmap.html', {'roadmap': roadmap, 'lines': lines})

# def show_roadmap(request, pk):
#     global roadmap_status

#     if pk in roadmap_status and roadmap_status[pk]:

#         roadmap_content = Roadmap.objects.get(project_id = pk)

#     return render(request, 'roadmap.html', {'roadmap':roadmap_content})

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname'] 
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome to GFG- Django Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to GFG!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nAnubhav Madhav"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ GFG - Django Login!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('signin')
        
        
    return render(request, "signin.html")

def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')
    
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "ongoing.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
    
    return render(request, "signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')