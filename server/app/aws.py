import os
import boto3
from pydantic import BaseModel

AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
AWS_COGNITO_APP_CLIENT_ID = os.getenv("AWS_COGNITO_APP_CLIENT_ID")
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