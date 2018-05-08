# -*- coding: utf-8 -*-
"""Model unit tests."""
import arrow
from datetime import datetime
from datetime import timedelta
import pytest
import pytz

from hxlti.consumer.models import Consumer
from hxlti.user.models import Role, User

from .factories import UserFactory


@pytest.mark.usefixtures('db')
class TestUser:
    """User tests."""

    def test_get_by_id(self):
        """Get user by ID."""
        user = User('foo', 'foo@bar.com')
        user.save()

        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self):
        """Test creation date."""
        user = User(username='foo', email='foo@bar.com')
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, datetime)

    def test_password_is_nullable(self):
        """Test null password."""
        user = User(username='foo', email='foo@bar.com')
        user.save()
        assert user.password is None

    def test_factory(self, db):
        """Test user factory."""
        user = UserFactory(password='myprecious')
        db.session.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created_at)
        assert user.is_admin is False
        assert user.active is True
        assert user.check_password('myprecious')

    def test_check_password(self):
        """Check password."""
        user = User.create(username='foo', email='foo@bar.com',
                           password='foobarbaz123')
        assert user.check_password('foobarbaz123') is True
        assert user.check_password('barfoobaz') is False

    def test_full_name(self):
        """User full name."""
        user = UserFactory(first_name='Foo', last_name='Bar')
        assert user.full_name == 'Foo Bar'

    def test_roles(self):
        """Add a role to a user."""
        role = Role(name='admin')
        role.save()
        user = UserFactory()
        user.roles.append(role)
        user.save()
        assert role in user.roles


@pytest.mark.usefixtures('db')
class TestConsumer:
    """Consumer tests."""

    def test_get_by_id(self):
        consumer = Consumer(
            client_key='a_consumer', secret_key='a_not_so_secret_secret_key')
        consumer.save()

        retrieved = Consumer.get_by_id(consumer.id)
        assert retrieved == consumer


    def test_consumer_with_defaults(self):
        now = arrow.utcnow()
        consumer = Consumer(client_key='x_consumer')
        consumer.save()

        # db has naive dates?
        #created_at = consumer.created_at.replace(tzinfo=pytz.utc)
        #expire_on = consumer.expire_on.replace(tzinfo=pytz.utc)

        assert (consumer.created_at - now) <= timedelta(seconds=1)  # close enough
        assert (consumer.expire_on - now) >= timedelta(weeks=4)  # magic number
        assert consumer.has_expired() is False
        assert consumer.client_key == 'x_consumer'
        assert consumer.secret_key is not None
        assert consumer.is_admin is False


    def test_expired_consumer(self):
        date_in_past = arrow.utcnow() - timedelta(days=2)
        consumer = Consumer(client_key='a_consumer', expire_on=date_in_past)
        consumer.save()

        assert consumer.has_expired()
