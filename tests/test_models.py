import pytest
# from posts.models import Post
from django.contrib.auth.models import User
# from posts.models import Post


@pytest.mark.django_db
def test_frontend():

    # Preparation phase
    user = User.objects.create_user('admin',is_superuser=True)
    # post = Post.objects.create(title='My new Post',author = user)

    # Assertion
    assert user.is_superuser == True
    assert user.username == 'admin'
    # assert post.title == 'My new Post'
    # assert post.author == user