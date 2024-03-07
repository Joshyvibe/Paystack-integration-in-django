from django.shortcuts import render, redirect
from django.contrib import auth, messages

from .forms import LoginForm, SignUpForm

from django.contrib.auth.models import User
from product.models import Product
from django.contrib.auth.decorators import login_required



@login_required
def account(request):
    return render(request, 'core/account.html')

def index(request):
    products = Product.objects.all()[0:10]
    return render(request, 'core/index.html', {'products': products})


def shop(request):
    products = Product.objects.all()
    context = { 
        'products': products,
    }
    return render(request, 'core/shop.html', context)


def about(request):
    return render(request, 'core/about.html')


def login(request):
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = auth.authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                auth.login(request, user)
                messages.success(request, f"Hello {user.username}! You have been logged in")
                return redirect("/")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = LoginForm()

    return render(request, "core/login.html", {"form": form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
           email = form.cleaned_data.get('email')
           if User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already registered, Please use a different email.')
           else:
                user = form.save()
                user.save()
               
                messages.success(request, f"New account created: Please login")
                return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
                
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})


def logout(request):
    auth.logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("index")



