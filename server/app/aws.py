import os
import boto3
from pydantic import BaseModel
import hmac
import hashlib
import base64

def get_secret_hash(client_id:str, client_secret: str, username:str):
  key = bytes(client_secret, 'utf-8')
  message = bytes(f'{username}{client_id}', 'utf-8')
  return base64.b64encode(hmac.new(key, message, digestmod=hashlib.sha256).digest()).decode()

  

AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
AWS_COGNITO_APP_CLIENT_ID = os.getenv("AWS_COGNITO_APP_CLIENT_ID")
AWS_COGNITO_APP_CLIENT_SECRET = os.getenv("AWS_COGNITO_APP_CLIENT_SECRET")
AWS_COGNITO_USER_POOL_ID = os.getenv("AWS_COGNITO_USER_POOL_ID")

class SignUpModel(BaseModel):
   full_name: str
   email: str
   password: str

class AWS_Cognito:
  def __init__(self):
    self.client = boto3.client("cognito-idp", region_name=AWS_REGION_NAME)

  def sign_up(self, user: SignUpModel):
    response = self.client.sign_up(
      ClientId=AWS_COGNITO_APP_CLIENT_ID,
      SecretHash=get_secret_hash(AWS_COGNITO_APP_CLIENT_ID, AWS_COGNITO_APP_CLIENT_SECRET, user.email),
      Username=user.email,
      Password=user.password,
      UserAttributes=[
        {
            'Name': 'name',
            'Value': user.full_name,
        },
        {
            'Name': 'custom:role',
            'Value': 'user'
        }
      ],
    )

    return response
  
def get_aws_cognito() -> AWS_Cognito:
  return AWS_Cognito()