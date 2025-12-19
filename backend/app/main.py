from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.service.user import UserServices
from app.models.user_model import register, login
import os
from app.pipeline.ingestion import upload as up

app = FastAPI(
    description="An intelligent document Parser",
    version=0.1
)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, 'index.html', {'message': 'message sent'} )

@app.post('/upload', response_class=HTMLResponse)
async def upload_files(request: Request, file: UploadFile = File(...)):
    try:
        result = await up.upload_file(file)
        if not result:
            return 'Upload Failed'
        # return 'File upload successfully'
        return result
    except Exception as e:
        return f"Error {e}"



# if __name__ == "__main__":
#     reg = register(
#         firstname='Tony',
#         lastname='John',
#         email='tony@gmail.com',
#         password='Password',
#         confirmPassword='Password'
#     )

#     log = login(
#         email='tony@gmail.com',
#         password='Password'        
#     )

#     # print(UserServices.createUser(user = reg))
#     print(UserServices.readUser(email= log.email, password=log.password))
#     # UserServices.deleteUser('1')
