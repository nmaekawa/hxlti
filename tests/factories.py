# -*- coding: utf-8 -*-
"""Factories to help in tests."""
import arrow
from datetime import timedelta

from factory import PostGenerationMethodCall, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from hxlti.database import db
from hxlti.consumer.models import Consumer
from hxlti.user.models import User


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    """User factory."""

    username = Sequence(lambda n: 'user{0}'.format(n))
    email = Sequence(lambda n: 'user{0}@example.com'.format(n))
    password = PostGenerationMethodCall('set_password', 'example')
    active = True

    class Meta:
        """Factory configuration."""

        model = User


class ConsumerFactory(BaseFactory):
    """Consumer factory."""

    client_key = Sequence(lambda n: 'client_key_{0}'.format(n))
    secret_key = Sequence(lambda n: 'client_secret_{0}'.format(n))
    created_at = arrow.utcnow()
    expire_on = arrow.utcnow() + timedelta(days=1)
    is_admin = False

    class Meta:
        model = Consumer
