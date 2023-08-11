from .models import Project, Roadmap
from django.shortcuts import render,redirect
import openai
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.models import User
from growthing import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse



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
        temperature=0.1,  
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