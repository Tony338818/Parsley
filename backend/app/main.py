from fastapi import FastAPI
from app.service.user import UserServices
from app.models.user_model import register, login

app = FastAPI(
    description="An intelligent document Parser",
    version=0.1
)

@app.get('/')
def home():
    return 'This is home to me'


if __name__ == "__main__":
    reg = register(
        firstname='Tony',
        lastname='John',
        email='tony@gmail.com',
        password='Password',
        confirmPassword='Password'
    )

    log = login(
        email='tony@gmail.com',
        password='Password'        
    )

    # print(UserServices.createUser(user = reg))
    print(UserServices.readUser(email= log.email, password=log.password))
    # UserServices.deleteUser('1')
