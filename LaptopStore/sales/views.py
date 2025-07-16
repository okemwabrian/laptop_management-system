from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Laptop, Sale, ContactMessage
from .forms import SaleForm, ContactForm, LaptopForm

# About Page
def about(request):
    return render(request, 'sales/about.html')

# Contact Page
def contact(request):
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )

            subject = f"New Contact Message from {form.cleaned_data['name']}"
            message = form.cleaned_data['message']
            sender_email = form.cleaned_data['email']
            recipient = ['youremail@example.com']  # 🔁 Replace with your real email

            try:
                send_mail(subject, message, sender_email, recipient, fail_silently=False)
            except Exception as e:
                print("Email send failed:", e)

            messages.success(request, "Your message has been sent!")
            return redirect('contact')

    return render(request, 'sales/contact.html', {'form': form})

# Laptop List
def laptop_list(request):
    query = request.GET.get('q')
    laptops = Laptop.objects.all()

    if query:
        laptops = laptops.filter(brand__icontains=query)

    return render(request, 'sales/laptop_list.html', {'laptops': laptops})

# Laptop Detail
def laptop_detail(request, laptop_id):
    laptop = get_object_or_404(Laptop, pk=laptop_id)
    form = SaleForm()

    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.laptop = laptop
            if sale.quantity > laptop.stock:
                messages.error(request, "Not enough stock!")
            else:
                laptop.stock -= sale.quantity
                laptop.save()
                sale.save()
                messages.success(request, "Purchase successful!")
                return redirect('laptop_detail', laptop_id=laptop.id)

    return render(request, 'sales/laptop_detail.html', {'laptop': laptop, 'form': form})

# Sales History (only accessible to logged-in users)
@login_required
def sales_history(request):
    sales = Sale.objects.select_related('laptop').order_by('-date')
    return render(request, 'sales/sales_history.html', {'sales': sales})

# User Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!")
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = UserCreationForm()
    
    return render(request, 'sales/register.html', {'form': form})

# User Login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('laptop_list')  
    else:
        form = AuthenticationForm()

    return render(request, 'sales/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('laptop_list')  

@login_required  
def add_laptop(request):
    if request.method == 'POST':
        form = LaptopForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            messages.success(request, "Laptop added successfully!")
            return redirect('laptop_list')
    else:
        form = LaptopForm()

    return render(request, 'sales/add_laptop.html', {'form': form})
