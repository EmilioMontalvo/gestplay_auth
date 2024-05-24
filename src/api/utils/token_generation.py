from itsdangerous import URLSafeTimedSerializer, BadTimeSignature,SignatureExpired
from pydantic import EmailStr
from ..schemas.profile import Profile
from ..schemas.token import ProfileToken
import os

token_algo= URLSafeTimedSerializer(os.getenv("EMAIL_SECRET"),salt='Email_Verification_&_Forgot_password')
def token(email: EmailStr):
    _token = token_algo.dumps(email)
    return _token

def verify_token(token:str):
    try:
      email = token_algo.loads(token, max_age=1800)
    except SignatureExpired:
       return None
    except BadTimeSignature:
     return None
    return {'email':email, 'check':True}

def profile_token(profile: Profile,email: EmailStr):

    profile_data = profile.model_dump()
    profile_data["email"] = email
    _token = token_algo.dumps(profile_data)
    return _token

def verify_profile_token(token:str):
    try:
      data = token_algo.loads(token, max_age=1800)
    except SignatureExpired:
       return None
    except BadTimeSignature:
     return None
    return data