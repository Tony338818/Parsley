from ..models.db_model import User, session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import hashlib
import bcrypt
from app import dependency


# def password_hashing_fucntion(password):
#     return hashlib.sha256(password.encode()).hexdigest()

def password_hashing_fucntion(password):
    code = str(password).encode('utf-8')
    salt = bcrypt.gensalt(12)

    hashed_password = bcrypt.hashpw(code, salt)
    return hashed_password

class UserServices():
    @staticmethod
    def get_user_by_email(email):
        return session.query(User).filter_by(email = email).first()
    
    def createUser(user):
        try:
            exists = UserServices.get_user_by_email(user.email)

            if exists:
                return "User with this email already exists"
            
            new_user = User(
                firstname = user.firstname,
                lastname = user.lastname,
                email = user.email,
                password = password_hashing_fucntion(user.password)
            )

            session.add(new_user)
            session.flush()
            session.commit()
            return f'New user created with id {new_user.id}, at {new_user.createdAt}'

        except IntegrityError as e:
            session.rollback()
            return f"Error: {e}"
        
        except SQLAlchemyError as e:
            session.rollback()
            return f"Error {e}"
        
    def readUser(email, password):
        user = UserServices.get_user_by_email(email)
        if not user:
            return "Account doesn't exist"
        
        p_code = str(password).encode('utf-8')
        if not bcrypt.checkpw(p_code, user.password):
            return "Invalid password"
        
        token = dependency.createToken(user_id= user.id, firstname=user.firstname)
        return user, token
    
    def updateUsers(user_id, data) :
        try:
            user = session.get(User, user_id)
            if not user:
                return None

            user.email = data.email
            user.firstname = data.firstname
            user.lastname = data.lastname
            user.password = password_hashing_fucntion(data.password)

            session.commit()
            return user

        except SQLAlchemyError as e:
            session.rollback()
            raise e

    # delete the data
    def deleteUser(user_id):
        user = session.get(User, user_id)
        if not user:
            return False

        session.delete(user)
        session.commit()
        return True

        
