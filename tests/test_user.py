import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_signup_view_post_valid_form(client):
    # Create a valid form data for signup
    form_data = {
        "username": "testuser",
        "password1": "testpassword",
        "password2": "testpassword"
    }

    # Send a POST request to the signup view with the form data
    response = client.post(reverse("signup"), form_data)

    # Check if the user was created successfully and redirected to the index page
    assert response.status_code == 302
    assert response.url == reverse("mainapp:index")

    # Check if the user was actually created in the database
    assert User.objects.filter(username="testuser").exists()

@pytest.mark.django_db
def test_signup_view_post_invalid_form(client):
    # Create an invalid form data for signup
    form_data = {
        "username": "testuser",
        "password1": "testpassword",
        "password2": "differentpassword"  # Passwords don't match
    }

    # Send a POST request to the signup view with the form data
    response = client.post(reverse("signup"), form_data)

    # Check if the form is displayed again with errors
    assert response.status_code == 200
    assert response.template_name == "signup.html"
    assert "The two password fields didn't match." in response.context_data["form"].errors["password2"]

    # Check if the user was not created in the database
    assert not User.objects.filter(username="testuser").exists()
