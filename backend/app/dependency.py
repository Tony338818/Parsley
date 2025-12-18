from jose import JWTError, jwt, ExpiredSignatureError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import datetime

security = HTTPBearer()
SECRET = "S0meSecretkeyForS0meReason"

# create token
def createToken(user_id, firstname):
    payload = {
        'user_id': user_id,
        'first_name': firstname,
        'exp': int((datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)).timestamp()),
        'random_stuff': 'TheMostRandomStuffYouHaveSeen'
    }

    token = jwt.encode(payload, SECRET, algorithm='HS256')
    return token

# Validate token
def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(
            token.credentials,
            SECRET,
            algorithms=["HS256"]
        )
        return payload  # contains userId, firstname, exp, randomstuff
    except ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except JWTError:
        raise HTTPException(401, "Invalid token")
