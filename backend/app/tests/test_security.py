from app.api.routes.auth import registerUser, loginUser
from app.models.user_model import register, login
from app.service.user import password_hashing_fucntion
from app.dependency import createToken
from bcrypt import checkpw, hashpw, gensalt


# Unit testing
def test_password_hash():
    """Test that the password hashes correctly"""
    password = "Password"
    hashedPassword = password_hashing_fucntion(password)

    assert hashedPassword is not None
    assert checkpw("Password".encode('utf-8'), hashedPassword) == True

def test_password_hash_different_passwords_different_hashes():
    """Test that hashing uses salt (different hashes each time)"""
    password = "SecurePassword123"
    hash1 = password_hashing_fucntion(password)
    hash2 = password_hashing_fucntion(password)
    
    assert hash1 != hash2 
    

def test_token_generation():
    """Test that a token is generated"""
    user_id = '#12'
    first_name = "John"

    token = createToken(user_id, first_name)

    assert token is not None
    assert isinstance(token, str)


# Intergration testing
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