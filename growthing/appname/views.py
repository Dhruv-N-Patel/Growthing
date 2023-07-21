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
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import redirect
import json
from django.urls import reverse
from json import dumps
from django.core.serializers import serialize


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
    user = request.user
    fname = user.first_name if user.is_authenticated else ""
    return render(request, "home.html",{"fname":fname})


def ongoing_project_list(request):
    projects = Roadmap.objects.all()
    programming = Roadmap.objects.filter(genre='programming')
    design = Roadmap.objects.filter(genre='design')
    marketing = Roadmap.objects.filter(genre='marketing')
    video_editing = Roadmap.objects.filter(genre='video editing')
    misc = Roadmap.objects.filter(genre='misc')
    return render(request, "home.html", context={'projects':projects, 'programming':programming, 'design':design,'marketing':marketing,'video_editing':video_editing, 'misc':misc})

def explore(request):
    context={
        
    }
    return render(request, "explore.html", context)

# def assistant(request):
#     context={
#     "previos_chatings1":"this is your previous chattings"
#     }
#     return render(request,'assistant.html', context)

def ongoing(request): 
    user= request.user
    ongoing_projects = Roadmap.objects.filter(user=request.user)
    # ongoing_projects = serialize('json', ongoing_projects)

    context= { 
        'ongoing_projects': ongoing_projects,
    }
    return render(request,'home.html', context)


    return render(request, 'home.html', context)

def index(request):
    context={
        "index_content":'index ka content'
    }
    messages.success(request, 'this is test message')
    return render(request, 'index.html', context)

def project_content(request,pk):
    project = Project.objects.get(project_id = pk)
    return render(request,'project.html', context={'project':project })

roadmap_status = {}
@login_required(login_url='/sigin')
def generate_roadmap(request,username, pk):
    global roadmap_status
    if request.method == 'POST':
       

        result = Roadmap(user=request.user)
        if request.user.is_authenticated:
            result.user = request.user
        result.save()

    if (username,pk) in roadmap_status and roadmap_status[(username, pk)]:
        url = reverse('roadmap', args=[username, pk])
        return redirect(url)
    
    else:
        api_key = settings.OPENAI_SETTINGS['api_key']
    
    openai.api_key = api_key
    # Retrieve projects from the database
    project = Project.objects.get(project_id = pk)

    json_string = '{ "Step_1" : [  "Task 1", "Task 2", "Task 3", "Task n" ], "Step_2" : [ "Task1", "Task2", "Task3", "Task n" ], "Step_3" : [ "Task1", "Task2", "Task3", "Task n" ] }'
    
    experience = request.POST.get('experience')
    expectation = request.POST.get('expectation')
    skills=request.POST.get('specific-skills')


    # Make request to OpenAI API
    response = openai.Completion.create( 

        engine="text-davinci-003",
        prompt=f" You are tutor that create roadmap for projects based on requirement of users.\
                 Project is in {project.genre} with title {project.title} \
                 Description of the project is {project.description}.\
                 Prior expience of user is {experience} and wants to {expectation}. User specifically want to learna and partice {skills}\
                 Make a very detailed roadmap for the project in such a way that user can learn the required skills and then implement them.\
                 Give the output only in JSON format with structure {json_string} and use make tasks if needed.\
                 Roadmap should be made for student to help them complete the project. Explain what to do, how can it be done. You must provide required resources links, tutorials links, documents and web links where ever required. \
                 Roadmap should be self-sufficient for all guidance that user might need during the excution.\
                ",
        #prompt=f"just say hey!", 
        max_tokens=3000,
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
        emoji = project.emoji,
        description = project.description,
        skills = project.skills,
        tools = project.tools,
        genre = project.genre,
        project_id = project.project_id,
        user=request.user,

    )
    roadmap.save()

    roadmap_status[(username, pk)] = True
    lines = roadmap.generate_roadmap.split('\n') 

    url = reverse('roadmap', args=[username, pk])

    return redirect(url)

roadmap_status = {}
def show_roadmap(request, username, pk):
        
    if (username,pk) in roadmap_status and roadmap_status[(username, pk)]:
        
        roadmap_content = Roadmap.objects.get(project_id=pk, user__username=username)
        lines = roadmap_content.generate_roadmap.split('\n')
        return render(request, 'roadmap.html', {'roadmap':roadmap_content, 'lines': lines, "user": request.user})

    # create data dictionary
    #     roadmap_content = Roadmap.objects.get(project_id = pk)
    #     dataDictionary = roadmap_content.generate_roadmap
    # # dump data
    #     dataJSON = dumps(dataDictionary)
    #     return render(request, 'roadmap.html', {'data': dataJSON})

    else : 
      url = reverse('generate_roadmap', args=[username, pk])
      return redirect(url)

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
        
        
        return redirect('signin')
        
        
    return render(request, "signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "home.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
    
    return render(request, "signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect("/")



# openai.api_key = settings.OPENAI_SETTINGS['api_key']

# class ResumeAssistantView(View):
#     template_name = 'resume_assistant.html'

#     def get(self, request):
#         context = {'chat_history': request.session.get('chat_history', [])}
#         return render(request, self.template_name, context)

#     def post(self, request):
#         chat_history = request.session.get('chat_history', [])
#         message = request.POST['message']

#         chat_history.append({'role': 'user', 'content': message})

#         if len(chat_history) > 4:
#             chat_history.pop(0)  # Remove oldest message if chat history exceeds 5 messages

#         response = openai.Completion.create(
#             engine='text-davinci-003',
#             prompt=self._build_prompt(chat_history),
#             temperature=0.7,
#             max_tokens=150,
#             n=1,
#             stop=None,
#         )

#         chat_history.append({'role': 'assistant', 'content': response.choices[0].text.strip()})

#         request.session['chat_history'] = chat_history

#         context = {'chat_history': chat_history}
#         return render(request, self.template_name, context)

#     def _build_prompt(self, chat_history):
#         # Building the prompt using chat history
#         prompt = "You are a resume assistant. You will help the student create a professional resume.\n"
#         for chat in chat_history:
#             role = chat['role']
#             content = chat['content']
#             prompt += f'{role}: {content}\n'

#         # Add customized prompts based on user responses
#         user_messages = [chat['content'] for chat in chat_history if chat['role'] == 'user']

#         # Field targeting prompt
#         if 'field' not in user_messages:
#             prompt += "Assistant: What field are you targeting in your resume? (e.g., consulting, product management, AI/ML, development, finance)\n"

#         # Resume preparation level prompt
#         elif 'resume preparation' not in user_messages:
#             prompt += "Assistant: What is the present level of your resume preparation?\n" \
#                       "1. Resume draft already made and needs improvement.\n" \
#                       "2. Pointers made but not started with making it into a resume and sections.\n" \
#                       "3. Need to start making it from scratch.\n"

#         # Sample resume prompt
#         elif 'sample resume' not in user_messages:
#             prompt += "Assistant: Do you have any sample resumes that you would like to take inspiration from?\n"

#         # Good things and improvements prompt
#         elif any(msg.startswith('sample resume:') for msg in user_messages):
#             prompt += "Assistant: What are the good things about that sample resume? " \
#                       "And what are the specific improvements you would like to make?\n"

#         # Section/pointer improvement prompt
#         else:
#             prompt += "Assistant: Which section or pointer would you like to improve? Or are you satisfied with the overall resume?\n"

#         prompt += "Assistant:"

#         return prompt
    
# class ClearChatView(View):
#     def get(self, request):
#         request.session['chat_history'] = []  # Clear the chat history
#         return redirect('resume_assistant')  # Redirect back to the main resume assistant view
    


def assistant(request):
    openai.api_key = settings.OPENAI_SETTINGS['api_key']
    chat_history = request.session.get('chat_history', [])
    message = request.POST['message']

    chat_history.append({'role': 'user', 'content': message})
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
       {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
    )

    # # print(completion.choices[0].message)
    chat_history.append({'role': 'assistant', 'content': completion.choices[0].text.strip()})

    request.session['chat_history'] = chat_history
    context = {'chat_history': chat_history}
    return(request, "assistant.html", context)