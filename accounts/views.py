from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login

def signup_view(request):
    if request.method == "POST":
        # User submitted the form, so process the data
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # If the form data is valid, save the new user to the database
            user = form.save()

            # Log in the newly registered user
            login(request, user)

            # Redirect the user to the "mainapp:index" URL after successful registration
            return redirect("mainapp:index")

        else:
            # If the form data is invalid, render the signup page with the form containing the errors
            form = UserCreationForm()
            return render(request, "signup.html", {"form": form})
    else:
        # This is a GET request, so show an empty signup form
        form = UserCreationForm()

    # Render the signup page with the form
    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        # User submitted the login form, so process the data
        signin_form = AuthenticationForm(data=request.POST)
        if signin_form.is_valid():
            # If the form data is valid, log in the user
            user = signin_form.get_user()
            login(request, user)

            # Redirect the user to the "mainapp:index" URL after successful login
            return redirect("mainapp:index")

    else:
        # This is a GET request, so show an empty login form
        signin_form = AuthenticationForm()

    # Render the login page with the form
    return render(request, "login.html", {"signin_form": signin_form})


def logout_view(request):
    if request.method == "POST":
        # User submitted a form or made a POST request
        logout(request)
        return redirect("mainapp:index")
    else:
        # This is a GET request
        logout(request)
        return redirect("mainapp:index")
