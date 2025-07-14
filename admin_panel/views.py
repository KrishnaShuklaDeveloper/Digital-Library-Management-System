from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

def is_admin(user):
    return user.is_authenticated and user.is_staff

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')  # Redirect logged-in admins to dashboard

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:  # Ensure only staff can log in
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials or you are not an admin.")

    return render(request, 'admin_panel/admin_login.html')

@login_required
@user_passes_test(is_admin, login_url='admin_login')
def admin_dashboard(request):
    return render(request, 'admin_panel/dashboard.html')

def admin_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('admin_login')
