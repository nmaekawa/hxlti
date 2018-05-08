"""consumer models."""
import arrow
from datetime import timedelta
from sqlalchemy_utils import ArrowType
from uuid import uuid4

from flask_login import UserMixin

from hxlti.database import Column, Model, SurrogatePK, db, reference_col, relationship
from hxlti.extensions import bcrypt



def expire_in_weeks(ttl=4):
    return arrow.utcnow() + timedelta(weeks=ttl)


def generate_id():
    return str(uuid4())


class Consumer(SurrogatePK, Model):
    """A consumer-secretkey pair for lti auth."""

    __tablename__ = 'consumers'
    client_key = Column(db.String(80), unique=True, nullable=False)
    secret_key = Column(db.String(128), nullable=False, default=generate_id)
    created_at = Column(ArrowType, nullable=False, default=arrow.utcnow)
    expire_on = Column(ArrowType, nullable=False, default=expire_in_weeks)
    is_admin = Column(db.Boolean(), default=False)


    def has_expired(self, now=None):
        if now is None:
            now = arrow.utcnow()
        return self.expire_on < now


    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Consumer({client_key!r})>'.format(client_key=self.client_key)

    def __str__(self):
        return self.client_key
