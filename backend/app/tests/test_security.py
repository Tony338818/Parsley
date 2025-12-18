from app.api.routes.auth import registerUser, loginUser
from app.models.user_model import register, login

def test_login():
    """Test that login function works with valid credentials"""
    user = login(
        email = 'tony@gmail.com', 
        password = 'Password'
    )

    result = loginUser(user)
    assert result is not None

def test_register():
    """Test that register function creates a new user"""
    user = register(
        firstname = 'Tony',
        lastname = 'John',
        email = 'tony@gmail.com',
        password = 'Password',
        confirmPassword= 'Password'
    )

    result = registerUser(user)
    assert result is not None