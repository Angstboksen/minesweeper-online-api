from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def CHECK_MASTER_TOKEN(giventoken):
    tokens = Token.objects.all()
    stafftokens = []
    for token in tokens:
        if(token.user.is_staff):
            stafftokens.append(token.key)
    return giventoken in stafftokens