import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User


def generate_jwt_token(user):
    """Generate JWT token for a user."""
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRATION_DELTA),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token


class JWTAuthentication(authentication.BaseAuthentication):
    """Custom JWT authentication class."""
    
    authentication_header_prefix = 'Bearer'
    
    def authenticate(self, request):
        """Authenticate the request and return a two-tuple of (user, token)."""
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header:
            return None
        
        auth_parts = auth_header.split()
        
        if len(auth_parts) != 2:
            return None
        
        prefix = auth_parts[0]
        token = auth_parts[1]
        
        if prefix.lower() != self.authentication_header_prefix.lower():
            return None
        
        return self._authenticate_credentials(token)
    
    def _authenticate_credentials(self, token):
        """Decode and validate the token, returning the user."""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired.')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token.')
        
        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found.')
        
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User is inactive.')
        
        return (user, token)
