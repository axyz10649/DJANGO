from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login')
def recipes(request):
    if request.method == 'POST':
        data = request.POST
        r_name = data.get('name')
        r_desp = data.get('desp')
        r_img = request.FILES.get('img')

        Recipe.objects.create(
            name = r_name,
            desp = r_desp,
            img = r_img,
        )
        return redirect('/')
    queryset = Recipe.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(name__icontains = request.GET.get('search'))

    context = {'recipes': queryset}
    return render(request, 'recipes.html', context)


def delete_recipe(request, id):
    queryset = Recipe.objects.get(id = id)
    queryset.delete()
    return redirect('/')

def update_recipe(request, id):
    queryset = Recipe.objects.get(id = id)
    if request.method == 'POST':
        data = request.POST
        r_name = data.get('name')
        r_desp = data.get('desp')
        r_img = request.FILES.get('img')
        queryset.name = r_name
        queryset.desp = r_desp
        if r_img:
            queryset.img = r_img
        
        queryset.save()
        return redirect('/')


    context = {'recipes': queryset}
    return render(request, 'update_recipe.html', context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists:
            messages.error(request, "Invalid username")
            return redirect('/login')
        
        user = authenticate(username = username, password = password)

        if not user:
            messages.error(request, "Invalid password")
            return redirect('/login')
        
        else:
            login(request, user)
            return redirect('/')


    return render(request, "login.html")

def logout_page(request):
    logout(request)
    return redirect('/login')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)

        if user.exists():
            messages.error(request, "User already exists.....")
            return redirect('/register')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account created successfully....")
        return redirect('/login')
    return render(request, "register.html")