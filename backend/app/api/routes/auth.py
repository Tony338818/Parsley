from ...models.user_model import register, login
from ...service.user import UserServices
from ...models.db_model import User

def registerUser(user: register):
    try:
        if user.password != user.confirmPassword:
            return 'Password does not match'
        result = UserServices.createUser(user)
        return result
    except Exception as e:
        return f'Error : {e}'

def loginUser(user: login):
    try:
        user, token = UserServices.readUser(user.email, user.password)
        if user is None:
            raise HTTPException(status_code=401, detail=account or "Invalid credentials")

        return {
                "message": "Login successful",
                "token": token,
                "user": {
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                    "email": user.email,
                }, }
    except Exception as e:
        return f'Error {e}'


