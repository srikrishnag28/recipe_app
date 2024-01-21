from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='login')
def Home(request):

    if request.method == 'POST':
        data = request.POST
        recipe_name = data['recipe_name']
        recipe_description = data['recipe_description']
        recipe_img = request.FILES['recipe_img']
        Recipe.objects.create(
            recipe_name=recipe_name,
            recipe_description=recipe_description,
            recipe_img=recipe_img
        )

        return redirect('recipe-home')
    recipies = Recipe.objects.all()

    if request.GET.get('search_recipe'):
        print(request.GET.get('search_recipe'))
        recipies = recipies.filter(recipe_name__icontains=request.GET.get('search_recipe'))
    return render(request, 'recipes.html', context={'recipies': recipies})

@login_required(login_url='login')
def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    recipe.delete()
    return redirect('recipe-home')

@login_required(login_url='login')
def update_recipe(request, id):

    recipe = get_object_or_404(Recipe, id=id)

    if request.method == 'POST':
        data = request.POST
        recipe_name = data['recipe_name']
        recipe_description = data['recipe_description']
        recipe.recipe_name = recipe_name
        recipe.recipe_description = recipe_description
        if 'recipe_img' in request.FILES:
            recipe_img = request.FILES['recipe_img']
            recipe.recipe_img = recipe_img
        recipe.save()
        return redirect('recipe-home')

    return render(request, 'update.html', context={'recipe': recipe})


def Login(request):

    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username!!')
            return redirect('login')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid Password!!')
            return redirect('login')

        login(request, user)
        next_url = request.GET.get('next', 'recipe-home')
        messages.success(request, 'Login Successfully!!')
        return redirect(next_url)

    return render(request, 'login.html')

def Logout(request):
    logout(request)
    messages.success(request, 'Logout Successfully!!')
    return redirect('login')

def Register(request):

    if request.method == 'POST':
        data = request.POST
        first_name = data['first_name']
        last_name = data['last_name']
        username = data['username']
        email = data['email']
        password = data['password']

        user = User.objects.filter(username=username)
        if user.exists():
            messages.error(request, 'Username already exist!!')
            return redirect('register')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            username = username
        )
        user.set_password(password)
        user.save()
        messages.success(request, 'Registered Successfully!!')
        return redirect('login')
    return render(request, 'register.html')
