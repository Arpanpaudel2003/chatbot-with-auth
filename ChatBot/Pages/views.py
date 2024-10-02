from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai

from django.contrib import auth
from django.contrib.auth.models import User

openai_api_key = 'your-api-key'
openai.api_key = openai_api_key

def ask_openai(message):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo', 
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ],
            max_tokens=150,
            temperature=0.7
        )

        answer = response['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        return f"Error: {str(e)}"

def home(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username,email,password1)
                user.save()
                auth.login(request,user)
                return redirect('home')
            except:
                error_message = 'i dont know what to tell you buddy'
                return render(request, 'register.html', {'error_message':error_message})

        else:
            error_message = 'passoword not matching dude'
            return render(request, 'register.html', {'error_message':error_message})
    return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            error_message = 'wrong username or password dumbass'
            return render(request,'login.html',{'error_message':error_message})
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
