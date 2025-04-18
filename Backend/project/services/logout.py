from project.tables import TokenBlocklist
from project.db import db

from datetime import timedelta
from datetime import datetime


def logout_logic(jti, expires_at):
  """Add token to the blocklist with its expiration time."""
  token = TokenBlocklist(jti=jti, expires_at=datetime.fromtimestamp(expires_at))
  db.session.add(token)
  db.session.commit()
  return {"message": "Logged out successfully"}
  
def is_token_revoked(jwt_payload):
  """Check if the token is in the blocklist."""
  jti = jwt_payload["jti"]
  token = TokenBlocklist.query.filter_by(jti=jti).first()
  return token is not None  # True if the token is revoked

def cleanup_expired_tokens():
  """Remove expired tokens from the blocklist."""
  now = datetime.utcnow()
  TokenBlocklist.query.filter(TokenBlocklist.expires_at < now).delete()
  db.session.commit()